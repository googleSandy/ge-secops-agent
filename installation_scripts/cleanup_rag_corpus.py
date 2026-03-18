#!/usr/bin/env python3
"""
RAG Corpus Cleanup Script

This script identifies actual runbook files vs cruft and provides tools to:
1. List files that should be kept vs removed
2. Sync only valid runbooks to GCS
3. Recreate the RAG corpus with clean data

Usage:
    python cleanup_rag_corpus.py analyze          # Show what will be kept/removed
    python cleanup_rag_corpus.py sync-to-gcs      # Upload only good files to GCS
    python cleanup_rag_corpus.py full-cleanup     # Complete cleanup workflow
"""

import os
from pathlib import Path
from typing import Annotated

import typer
from dotenv import load_dotenv
from google.auth import default
from google.cloud import storage


app = typer.Typer(
    add_completion=False,
    help="Clean up RAG corpus by removing cruft and keeping only actual runbooks.",
)

# Patterns for files/directories to EXCLUDE (cruft)
EXCLUDE_PATTERNS = [
    # SOAR integration API docs (not runbooks)
    "**/soar_integrations/**",
    "**/soar_integrations",
    # Framework/project files
    "**/SuperClaude_Framework/**",
    "**/SuperClaude/**",
    # Generated reports (examples, not runbooks)
    "**/reports/**",
    # MCP server documentation
    "**/mcp-security/docs/servers/**",
    "**/mcp-security/server/**",
    "**/mcp-security/run-with-google-adk/**",
    # Project meta files
    "CODE_OF_CONDUCT.md",
    "CONTRIBUTING.md",
    "CONTRIBUTING",
    "LICENSE",
    "LICENSE.md",
    "CHANGELOG.md",
    "ROADMAP.md",
    "SECURITY.md",
    "MANIFEST.in",
    "VERSION",
    "README.md",
    "readme.md",
    "SETUP_CLAUDE.md",
    "SUPERCLAUDE_INTEGRATION_SUMMARY.md",
    "LLMS.md",
    "LLMS-THESAURUS.md",
    "LLMS-SITEMAP.md",
    "CLAUDE.md",
    "GEMINI.md",
    "EXAMPLE_PROMPTS.md",
    # Config/build files
    "pyproject.toml",
    "setup.py",
    "uv.lock",
    "requirements*.txt",
    "Makefile",
    "*.sh",
    # Hidden directories
    ".*/**",
    ".github/**",
    ".claude/**",
    ".clinerules/**",
    ".gemini/**",
    # External/nested submodules (already have mcp-security at top level)
    "**/external/**",
    # Test files
    "**/tests/**",
]

# Directories containing actual runbooks to INCLUDE
INCLUDE_DIRECTORIES = [
    # ai-runbooks actual runbooks
    "ai-runbooks/rules_bank/run_books",
    "ai-runbooks/rules_bank/personas",
    "ai-runbooks/rules_bank/run_books/common_steps",
    "ai-runbooks/rules_bank/run_books/irps",
    "ai-runbooks/rules_bank/run_books/guidelines",
    # adk_runbooks actual runbooks
    "adk_runbooks/rules-bank/run_books",
    "adk_runbooks/rules-bank/personas",
    "adk_runbooks/rules-bank/run_books/common_steps",
    "adk_runbooks/rules-bank/run_books/irps",
    "adk_runbooks/rules-bank/run_books/guidelines",
    "adk_runbooks/rules-bank/atomic_runbooks",
    "adk_runbooks/rules-bank/ai",
    "adk_runbooks/rules-bank/multi_agent",
    "adk_runbooks/rules-bank/tools",
]


class RAGCleanup:
    """Manages RAG corpus cleanup operations."""

    def __init__(self, project_root: Path, env_file: Path):
        self.project_root = project_root
        self.env_file = env_file
        self.env_vars = self._load_env_vars()
        self.storage_client = None

    def _load_env_vars(self) -> dict[str, str]:
        """Load environment variables from .env file."""
        if self.env_file.exists():
            load_dotenv(self.env_file, override=True)
        return dict(os.environ)

    def _init_gcs(self) -> None:
        """Initialize GCS client."""
        if self.storage_client:
            return
        try:
            credentials, _ = default()
            self.storage_client = storage.Client(
                project=self.env_vars.get("GCP_PROJECT_ID"),
                credentials=credentials,
            )
        except Exception as e:
            typer.secho(f"Failed to initialize GCS: {e}", fg=typer.colors.RED)
            raise typer.Exit(code=1)

    def _should_exclude(self, file_path: Path) -> bool:
        """Check if a file should be excluded based on patterns."""
        rel_path = file_path.relative_to(self.project_root)
        str_path = str(rel_path)
        name = file_path.name

        # Check filename exclusions
        for pattern in EXCLUDE_PATTERNS:
            if not pattern.startswith("*"):
                if name == pattern:
                    return True

        # Check path pattern exclusions
        for pattern in EXCLUDE_PATTERNS:
            if "**" in pattern or "*" in pattern:
                # Simple glob matching
                pattern_parts = pattern.replace("**", "*").split("/")
                path_parts = str_path.split("/")

                for i, part in enumerate(pattern_parts):
                    if part == "*":
                        continue
                    if "*" in part:
                        # Wildcard in part
                        import fnmatch

                        if any(fnmatch.fnmatch(p, part) for p in path_parts):
                            if pattern.endswith("/**") or pattern.endswith("/*"):
                                return True
                    elif part in path_parts:
                        if pattern.endswith("/**"):
                            return True

        # More specific checks
        if "soar_integrations" in str_path:
            return True
        if "SuperClaude" in str_path:
            return True
        if "/reports/" in str_path or str_path.startswith("reports/"):
            return True
        if "/external/" in str_path:
            return True
        if "mcp-security/docs/servers" in str_path:
            return True
        if "mcp-security/server" in str_path:
            return True
        if str_path.startswith("."):
            return True

        return False

    def _is_in_include_directory(self, file_path: Path) -> bool:
        """Check if file is in an explicitly included directory."""
        rel_path = str(file_path.relative_to(self.project_root))
        for inc_dir in INCLUDE_DIRECTORIES:
            if rel_path.startswith(inc_dir):
                return True
        return False

    def get_all_markdown_files(self) -> list[Path]:
        """Get all markdown files in the project."""
        files = []
        for source_dir in ["ai-runbooks", "adk_runbooks"]:
            source_path = self.project_root / source_dir
            if source_path.exists():
                files.extend(source_path.rglob("*.md"))
        return sorted(files)

    def categorize_files(self) -> tuple[list[Path], list[Path]]:
        """Categorize files into keep and remove lists."""
        keep = []
        remove = []

        for file_path in self.get_all_markdown_files():
            if self._should_exclude(file_path):
                remove.append(file_path)
            elif self._is_in_include_directory(file_path):
                keep.append(file_path)
            else:
                # Not explicitly included, check if it looks like a runbook
                remove.append(file_path)

        return keep, remove

    def analyze(self, verbose: bool = False) -> None:
        """Analyze and display categorization of files."""
        keep, remove = self.categorize_files()

        typer.echo("\n" + "=" * 80)
        typer.secho("RAG CORPUS CLEANUP ANALYSIS", fg=typer.colors.CYAN, bold=True)
        typer.echo("=" * 80)

        typer.echo(f"\nTotal markdown files found: {len(keep) + len(remove)}")
        typer.secho(
            f"Files to KEEP (actual runbooks): {len(keep)}", fg=typer.colors.GREEN
        )
        typer.secho(f"Files to REMOVE (cruft): {len(remove)}", fg=typer.colors.RED)
        typer.echo(
            f"\nReduction: {len(remove)} files ({100*len(remove)//(len(keep)+len(remove))}%)"
        )

        if verbose:
            typer.echo("\n" + "-" * 40)
            typer.secho("FILES TO KEEP:", fg=typer.colors.GREEN, bold=True)
            typer.echo("-" * 40)
            for f in keep:
                typer.echo(f"  {f.relative_to(self.project_root)}")

            typer.echo("\n" + "-" * 40)
            typer.secho("FILES TO REMOVE:", fg=typer.colors.RED, bold=True)
            typer.echo("-" * 40)
            for f in remove:
                typer.echo(f"  {f.relative_to(self.project_root)}")

        # Show breakdown by category
        typer.echo("\n" + "-" * 40)
        typer.echo("REMOVAL BREAKDOWN BY CATEGORY:")
        typer.echo("-" * 40)

        categories = {
            "soar_integrations": 0,
            "SuperClaude": 0,
            "reports": 0,
            "mcp-security/docs": 0,
            "external": 0,
            "root_level": 0,
            "other": 0,
        }

        for f in remove:
            rel = str(f.relative_to(self.project_root))
            if "soar_integrations" in rel:
                categories["soar_integrations"] += 1
            elif "SuperClaude" in rel:
                categories["SuperClaude"] += 1
            elif "/reports/" in rel or rel.endswith("/reports"):
                categories["reports"] += 1
            elif "mcp-security/docs" in rel:
                categories["mcp-security/docs"] += 1
            elif "/external/" in rel:
                categories["external"] += 1
            elif rel.count("/") <= 1:
                categories["root_level"] += 1
            else:
                categories["other"] += 1

        for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
            if count > 0:
                typer.echo(f"  {cat}: {count}")

    def sync_to_gcs(
        self,
        bucket_name: str | None = None,
        prefix: str = "rag-runbooks-clean",
        dry_run: bool = False,
    ) -> list[str]:
        """Sync only good runbook files to GCS."""
        self._init_gcs()

        bucket_name = bucket_name or self.env_vars.get(
            "GCP_STAGING_BUCKET", ""
        ).replace("gs://", "")
        if not bucket_name:
            typer.secho(
                "No bucket specified and GCP_STAGING_BUCKET not set",
                fg=typer.colors.RED,
            )
            raise typer.Exit(code=1)

        keep, _ = self.categorize_files()

        typer.echo(
            f"\nSyncing {len(keep)} runbook files to gs://{bucket_name}/{prefix}/"
        )

        if dry_run:
            typer.secho("\n[DRY RUN] Would upload:", fg=typer.colors.YELLOW)
            for f in keep:
                typer.echo(f"  {f.relative_to(self.project_root)}")
            return []

        bucket = self.storage_client.bucket(bucket_name)
        uploaded_uris = []

        for file_path in keep:
            rel_path = file_path.relative_to(self.project_root)
            blob_name = f"{prefix}/{rel_path}"
            blob = bucket.blob(blob_name)

            typer.echo(f"  Uploading: {rel_path}")
            blob.upload_from_filename(str(file_path))
            uploaded_uris.append(f"gs://{bucket_name}/{blob_name}")

        typer.secho(
            f"\nUploaded {len(uploaded_uris)} files to GCS", fg=typer.colors.GREEN
        )
        return uploaded_uris

    def generate_import_commands(self, gcs_prefix: str = "rag-runbooks-clean") -> None:
        """Generate the make commands to recreate the RAG corpus."""
        bucket = self.env_vars.get("GCP_STAGING_BUCKET", "gs://YOUR_BUCKET")
        corpus_id = self.env_vars.get("RAG_CORPUS_ID", "YOUR_CORPUS_ID")

        typer.echo("\n" + "=" * 80)
        typer.secho("CLEANUP COMMANDS", fg=typer.colors.CYAN, bold=True)
        typer.echo("=" * 80)

        typer.echo("\n1. Delete the old RAG corpus:")
        typer.secho(
            f"   make rag-delete RAG_CORPUS_ID={corpus_id} FORCE=1",
            fg=typer.colors.YELLOW,
        )

        typer.echo("\n2. Create a new clean RAG corpus:")
        typer.secho(
            '   make rag-create NAME="Agentic SOC Runbooks (Clean)" DESC="Curated security runbooks only"',
            fg=typer.colors.YELLOW,
        )

        typer.echo("\n3. Import the clean files (after getting new corpus ID):")
        typer.secho(
            f'   make rag-import RAG_CORPUS_ID=<NEW_CORPUS_ID> GCS_URI="{bucket}/{gcs_prefix}/"',
            fg=typer.colors.YELLOW,
        )

        typer.echo("\n4. Update .env with the new RAG_CORPUS_ID")

        typer.echo("\n5. Redeploy the agent:")
        typer.secho("   make agent-engine-redeploy", fg=typer.colors.YELLOW)


@app.command()
def analyze(
    verbose: Annotated[
        bool, typer.Option("--verbose", "-v", help="Show all files")
    ] = False,
    env_file: Annotated[Path, typer.Option(help="Path to .env file")] = Path(".env"),
) -> None:
    """Analyze files and show what would be kept vs removed."""
    project_root = Path.cwd()
    cleanup = RAGCleanup(project_root, env_file)
    cleanup.analyze(verbose)
    cleanup.generate_import_commands()


@app.command()
def sync_to_gcs(
    bucket: Annotated[str | None, typer.Option(help="GCS bucket name")] = None,
    prefix: Annotated[
        str, typer.Option(help="GCS prefix for uploaded files")
    ] = "rag-runbooks-clean",
    dry_run: Annotated[
        bool, typer.Option("--dry-run", "-n", help="Show what would be uploaded")
    ] = False,
    env_file: Annotated[Path, typer.Option(help="Path to .env file")] = Path(".env"),
) -> None:
    """Upload only valid runbook files to GCS."""
    project_root = Path.cwd()
    cleanup = RAGCleanup(project_root, env_file)
    cleanup.sync_to_gcs(bucket, prefix, dry_run)


@app.command()
def full_cleanup(
    bucket: Annotated[str | None, typer.Option(help="GCS bucket name")] = None,
    prefix: Annotated[
        str, typer.Option(help="GCS prefix for uploaded files")
    ] = "rag-runbooks-clean",
    env_file: Annotated[Path, typer.Option(help="Path to .env file")] = Path(".env"),
) -> None:
    """Run full cleanup workflow: analyze, sync to GCS, show commands."""
    project_root = Path.cwd()
    cleanup = RAGCleanup(project_root, env_file)

    # Step 1: Analyze
    cleanup.analyze(verbose=False)

    # Step 2: Confirm
    if not typer.confirm("\nProceed with uploading clean files to GCS?"):
        typer.echo("Cancelled.")
        raise typer.Exit(code=0)

    # Step 3: Sync to GCS
    cleanup.sync_to_gcs(bucket, prefix, dry_run=False)

    # Step 4: Show next steps
    cleanup.generate_import_commands(prefix)


if __name__ == "__main__":
    app()
