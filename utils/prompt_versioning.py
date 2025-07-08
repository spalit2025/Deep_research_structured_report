#!/usr/bin/env python3
"""
Prompt Versioning System
Manages multiple versions of prompts with performance tracking and A/B testing capabilities
"""

from dataclasses import asdict, dataclass
from datetime import datetime
import json
import logging
import os
import time
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)


@dataclass
class PromptVersion:
    """A single version of a prompt with metadata"""

    version: str
    prompt_text: str
    created_at: float
    description: str
    is_active: bool = True
    usage_count: int = 0
    success_rate: float = 0.0
    avg_quality_score: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class PromptUsage:
    """Records usage and performance of a prompt version"""

    version: str
    timestamp: float
    success: bool
    quality_score: float
    execution_time: float
    template_type: str
    section_type: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


@dataclass
class PromptPerformanceMetrics:
    """Aggregated performance metrics for a prompt version"""

    version: str
    total_usage: int
    success_rate: float
    avg_quality_score: float
    avg_execution_time: float
    last_used: float

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)


class PromptVersionManager:
    """Manages versioned prompts with performance tracking"""

    def __init__(
        self,
        versions_dir: str = "prompt_versions",
        usage_log_file: str = "prompt_usage.json",
        enable_analytics: bool = True,
    ):
        """
        Initialize prompt version manager

        Args:
            versions_dir: Directory to store prompt versions
            usage_log_file: File to log prompt usage analytics
            enable_analytics: Whether to track usage and performance
        """
        self.versions_dir = versions_dir
        self.usage_log_file = usage_log_file
        self.enable_analytics = enable_analytics

        # In-memory storage
        self.prompts: Dict[
            str, Dict[str, PromptVersion]
        ] = {}  # prompt_name -> version -> PromptVersion
        self.usage_history: List[PromptUsage] = []

        # Create directories
        os.makedirs(versions_dir, exist_ok=True)

        # Load existing data
        self._load_versions()
        self._load_usage_history()

        logger.info(
            f"PromptVersionManager initialized with {len(self.prompts)} prompt types"
        )

    def add_prompt_version(
        self, prompt_name: str, version: str, prompt_text: str, description: str = ""
    ) -> bool:
        """
        Add a new version of a prompt

        Args:
            prompt_name: Name/identifier of the prompt
            version: Version identifier (e.g., "v1.0", "experimental")
            prompt_text: The actual prompt text
            description: Description of changes/purpose

        Returns:
            True if added successfully, False if version already exists
        """
        if prompt_name not in self.prompts:
            self.prompts[prompt_name] = {}

        if version in self.prompts[prompt_name]:
            logger.warning(f"Version {version} of prompt {prompt_name} already exists")
            return False

        prompt_version = PromptVersion(
            version=version,
            prompt_text=prompt_text,
            created_at=time.time(),
            description=description,
        )

        self.prompts[prompt_name][version] = prompt_version
        self._save_version(prompt_name, prompt_version)

        logger.info(f"Added prompt {prompt_name} version {version}")
        return True

    def get_prompt(
        self,
        prompt_name: str,
        version: Optional[str] = None,
        fallback_to_active: bool = True,
    ) -> Optional[str]:
        """
        Get a specific version of a prompt

        Args:
            prompt_name: Name of the prompt
            version: Specific version to get (None for active version)
            fallback_to_active: If version not found, try to get active version

        Returns:
            Prompt text or None if not found
        """
        if prompt_name not in self.prompts:
            logger.warning(f"Prompt {prompt_name} not found")
            return None

        # If no version specified, get the active version
        if version is None:
            version = self._get_active_version(prompt_name)
            if version is None:
                logger.warning(f"No active version found for prompt {prompt_name}")
                return None

        # Try to get the specific version
        if version in self.prompts[prompt_name]:
            prompt_version = self.prompts[prompt_name][version]

            # Update usage count
            if self.enable_analytics:
                prompt_version.usage_count += 1

            return prompt_version.prompt_text

        # Fallback to active version if requested
        if fallback_to_active and version != self._get_active_version(prompt_name):
            active_version = self._get_active_version(prompt_name)
            if active_version:
                logger.info(
                    f"Version {version} not found, using active version {active_version}"
                )
                return self.get_prompt(
                    prompt_name, active_version, fallback_to_active=False
                )

        logger.warning(f"Version {version} of prompt {prompt_name} not found")
        return None

    def set_active_version(self, prompt_name: str, version: str) -> bool:
        """
        Set the active version for a prompt

        Args:
            prompt_name: Name of the prompt
            version: Version to make active

        Returns:
            True if successful, False otherwise
        """
        if prompt_name not in self.prompts or version not in self.prompts[prompt_name]:
            logger.error(f"Prompt {prompt_name} version {version} not found")
            return False

        # Deactivate all versions
        for v in self.prompts[prompt_name].values():
            v.is_active = False

        # Activate the specified version
        self.prompts[prompt_name][version].is_active = True

        # Save changes
        for v in self.prompts[prompt_name].values():
            self._save_version(prompt_name, v)

        logger.info(f"Set {prompt_name} active version to {version}")
        return True

    def log_usage(
        self,
        prompt_name: str,
        version: str,
        success: bool,
        quality_score: float = 0.0,
        execution_time: float = 0.0,
        template_type: str = "unknown",
        section_type: str = "unknown",
    ) -> None:
        """
        Log usage of a prompt version for analytics

        Args:
            prompt_name: Name of the prompt used
            version: Version used
            success: Whether the prompt usage was successful
            quality_score: Quality score (0.0-1.0)
            execution_time: Time taken to execute
            template_type: Type of template (business, academic, etc.)
            section_type: Type of section (introduction, conclusion, etc.)
        """
        if not self.enable_analytics:
            return

        usage = PromptUsage(
            version=f"{prompt_name}:{version}",
            timestamp=time.time(),
            success=success,
            quality_score=quality_score,
            execution_time=execution_time,
            template_type=template_type,
            section_type=section_type,
        )

        self.usage_history.append(usage)

        # Update prompt version metrics
        if prompt_name in self.prompts and version in self.prompts[prompt_name]:
            prompt_version = self.prompts[prompt_name][version]

            # Calculate running averages
            total_usage = prompt_version.usage_count
            if total_usage > 0:
                # Update success rate
                current_successes = prompt_version.success_rate * (total_usage - 1)
                new_successes = current_successes + (1 if success else 0)
                prompt_version.success_rate = new_successes / total_usage

                # Update quality score
                current_quality = prompt_version.avg_quality_score * (total_usage - 1)
                new_quality = current_quality + quality_score
                prompt_version.avg_quality_score = new_quality / total_usage

        # Periodically save usage history
        if len(self.usage_history) % 10 == 0:  # Save every 10 entries
            self._save_usage_history()

    def get_performance_metrics(
        self, prompt_name: str
    ) -> Dict[str, PromptPerformanceMetrics]:
        """
        Get performance metrics for all versions of a prompt

        Args:
            prompt_name: Name of the prompt

        Returns:
            Dictionary mapping version to performance metrics
        """
        if prompt_name not in self.prompts:
            return {}

        metrics = {}
        for version, prompt_version in self.prompts[prompt_name].items():
            # Find usage entries for this prompt version
            version_key = f"{prompt_name}:{version}"
            version_usage = [u for u in self.usage_history if u.version == version_key]

            if version_usage:
                avg_execution_time = sum(u.execution_time for u in version_usage) / len(
                    version_usage
                )
                last_used = max(u.timestamp for u in version_usage)
            else:
                avg_execution_time = 0.0
                last_used = prompt_version.created_at

            metrics[version] = PromptPerformanceMetrics(
                version=version,
                total_usage=prompt_version.usage_count,
                success_rate=prompt_version.success_rate,
                avg_quality_score=prompt_version.avg_quality_score,
                avg_execution_time=avg_execution_time,
                last_used=last_used,
            )

        return metrics

    def get_best_performing_version(self, prompt_name: str) -> Optional[str]:
        """
        Get the best performing version of a prompt based on composite score

        Args:
            prompt_name: Name of the prompt

        Returns:
            Version string of best performing version, or None if no data
        """
        metrics = self.get_performance_metrics(prompt_name)
        if not metrics:
            return None

        best_version = None
        best_score = -1.0

        for version, metric in metrics.items():
            if metric.total_usage < 5:  # Need minimum usage for reliable metrics
                continue

            # Composite score: 40% success rate + 40% quality + 20% usage frequency
            score = (
                0.4 * metric.success_rate
                + 0.4 * metric.avg_quality_score
                + 0.2 * min(1.0, metric.total_usage / 100)
            )

            if score > best_score:
                best_score = score
                best_version = version

        return best_version

    def create_performance_report(self, prompt_name: str = None) -> str:
        """
        Create a detailed performance report

        Args:
            prompt_name: Specific prompt to report on (None for all prompts)

        Returns:
            Formatted performance report
        """
        report_lines = ["# Prompt Performance Report", ""]
        report_lines.append(
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        )
        report_lines.append("")

        prompts_to_report = [prompt_name] if prompt_name else list(self.prompts.keys())

        for pname in prompts_to_report:
            if pname not in self.prompts:
                continue

            report_lines.append(f"## Prompt: {pname}")
            report_lines.append("")

            metrics = self.get_performance_metrics(pname)
            active_version = self._get_active_version(pname)
            best_version = self.get_best_performing_version(pname)

            if active_version:
                report_lines.append(f"**Active Version**: {active_version}")
            if best_version:
                report_lines.append(f"**Best Performing**: {best_version}")
            report_lines.append("")

            # Version comparison table
            if metrics:
                report_lines.append(
                    "| Version | Usage | Success Rate | Quality Score | Last Used |"
                )
                report_lines.append(
                    "|---------|-------|--------------|---------------|-----------|"
                )

                for version, metric in sorted(
                    metrics.items(), key=lambda x: x[1].total_usage, reverse=True
                ):
                    last_used_str = datetime.fromtimestamp(metric.last_used).strftime(
                        "%Y-%m-%d"
                    )
                    report_lines.append(
                        f"| {version} | {metric.total_usage} | "
                        f"{metric.success_rate:.1%} | {metric.avg_quality_score:.2f} | {last_used_str} |"
                    )
                report_lines.append("")

            report_lines.append("")

        return "\n".join(report_lines)

    def _get_active_version(self, prompt_name: str) -> Optional[str]:
        """Get the active version for a prompt"""
        if prompt_name not in self.prompts:
            return None

        for version, prompt_version in self.prompts[prompt_name].items():
            if prompt_version.is_active:
                return version

        # If no active version, return the latest
        if self.prompts[prompt_name]:
            return max(
                self.prompts[prompt_name].keys(),
                key=lambda v: self.prompts[prompt_name][v].created_at,
            )

        return None

    def _save_version(self, prompt_name: str, prompt_version: PromptVersion) -> None:
        """Save a prompt version to disk"""
        filename = f"{prompt_name}_{prompt_version.version}.json"
        filepath = os.path.join(self.versions_dir, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(prompt_version.to_dict(), f, indent=2)

    def _load_versions(self) -> None:
        """Load all prompt versions from disk"""
        if not os.path.exists(self.versions_dir):
            return

        for filename in os.listdir(self.versions_dir):
            if filename.endswith(".json"):
                try:
                    filepath = os.path.join(self.versions_dir, filename)
                    with open(filepath, encoding="utf-8") as f:
                        data = json.load(f)

                    prompt_version = PromptVersion(**data)

                    # Extract prompt name from filename
                    prompt_name = filename.replace(
                        f"_{prompt_version.version}.json", ""
                    )

                    if prompt_name not in self.prompts:
                        self.prompts[prompt_name] = {}

                    self.prompts[prompt_name][prompt_version.version] = prompt_version

                except Exception as e:
                    logger.warning(
                        f"Failed to load prompt version from {filename}: {e}"
                    )

    def _save_usage_history(self) -> None:
        """Save usage history to disk"""
        try:
            with open(self.usage_log_file, "w", encoding="utf-8") as f:
                json.dump(
                    [usage.to_dict() for usage in self.usage_history], f, indent=2
                )
        except Exception as e:
            logger.warning(f"Failed to save usage history: {e}")

    def _load_usage_history(self) -> None:
        """Load usage history from disk"""
        if not os.path.exists(self.usage_log_file):
            return

        try:
            with open(self.usage_log_file, encoding="utf-8") as f:
                data = json.load(f)

            self.usage_history = [PromptUsage(**entry) for entry in data]
            logger.info(f"Loaded {len(self.usage_history)} usage history entries")

        except Exception as e:
            logger.warning(f"Failed to load usage history: {e}")


# Global instance
_prompt_version_manager = None


def get_prompt_version_manager(config: Dict[str, Any] = None) -> PromptVersionManager:
    """Get or create the global prompt version manager"""
    global _prompt_version_manager

    if _prompt_version_manager is None:
        if config:
            versions_dir = config.get("prompt_versions_dir", "prompt_versions")
            usage_log = config.get("prompt_usage_log", "prompt_usage.json")
            enable_analytics = config.get("enable_prompt_analytics", True)
        else:
            versions_dir = "prompt_versions"
            usage_log = "prompt_usage.json"
            enable_analytics = True

        _prompt_version_manager = PromptVersionManager(
            versions_dir=versions_dir,
            usage_log_file=usage_log,
            enable_analytics=enable_analytics,
        )

    return _prompt_version_manager
