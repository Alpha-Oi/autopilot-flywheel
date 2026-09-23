<#
.SYNOPSIS
    Phase 0 verification scaffold for Autopilot Flywheel.

.DESCRIPTION
    Этот скрипт намеренно НЕ запускает предполагаемые команды сторонних инструментов.
    До подтверждения CLI/API по pinned upstream version такие команды считаются гипотезами.

    Скрипт показывает обязательный verification matrix и ссылки на upstream.
    Фактические probes добавляются только после evidence review.
#>

$ErrorActionPreference = "Stop"

Write-Host "Autopilot Flywheel — Phase 0 Integration Verification" -ForegroundColor Cyan
Write-Host "Mode: evidence-first / non-destructive" -ForegroundColor Yellow
Write-Host ""

$checks = @(
    @{ Name = "Beads Workflow"; Repo = "Dicklesworthstone/beads-workflow"; Status = "PROPOSED" },
    @{ Name = "Beads Viewer"; Repo = "Dicklesworthstone/beads_viewer"; Status = "PROPOSED" },
    @{ Name = "NTM"; Repo = "Dicklesworthstone/named_tmux_manager"; Status = "PROPOSED" },
    @{ Name = "MCP Agent Mail"; Repo = "Dicklesworthstone/mcp_agent_mail"; Status = "PROPOSED" },
    @{ Name = "DCG"; Repo = "Dicklesworthstone/destructive_command_guard"; Status = "PROPOSED" },
    @{ Name = "CASS"; Repo = "Dicklesworthstone/coding_agent_session_search"; Status = "PROPOSED" },
    @{ Name = "CASS Memory"; Repo = "Dicklesworthstone/cass_memory_system"; Status = "PROPOSED" },
    @{ Name = "ACFS"; Repo = "Dicklesworthstone/agentic_coding_flywheel_setup"; Status = "PROPOSED" }
)

foreach ($c in $checks) {
    Write-Host "[$($c.Status)] $($c.Name)" -ForegroundColor Magenta
    Write-Host "  https://github.com/$($c.Repo)"
    Write-Host "  [ ] pin version/tag"
    Write-Host "  [ ] record commit SHA"
    Write-Host "  [ ] inspect official docs/source"
    Write-Host "  [ ] observe real capability surface"
    Write-Host "  [ ] record inputs/outputs/errors"
    Write-Host "  [ ] review security/state/concurrency"
    Write-Host "  [ ] update docs/INTERFACES.md"
    Write-Host ""
}

Write-Host "Protocol: docs/VERIFICATION.md" -ForegroundColor Cyan
Write-Host "No external commands were executed." -ForegroundColor Green
