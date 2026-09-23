<#
.SYNOPSIS
    Верификация интеграции Autopilot Flywheel.
.DESCRIPTION
    Запускать ПОСЛЕ завершения https://github.com/Alpha-Oi/autopilot-jet.
#>

Write-Host "Верификация интеграций Autopilot Flywheel" -ForegroundColor Cyan
Write-Host "Запускать только после завершения autopilot-jet!" -ForegroundColor Yellow
Write-Host ""

$checks = @(
    @{ Name = "DCG";            Repo = "Dicklesworthstone/destructive_command_guard";      API = "dcg --version" },
    @{ Name = "CASS";           Repo = "Dicklesworthstone/coding_agent_session_search";   API = "cass --version" },
    @{ Name = "CASS Memory";    Repo = "Dicklesworthstone/cass_memory_system";            API = "cm --version" },
    @{ Name = "Beads Viewer";   Repo = "Dicklesworthstone/beads_viewer";                  API = "bv --version" },
    @{ Name = "Beads Workflow"; Repo = "Dicklesworthstone/beads-workflow";                API = "beads-workflow --version" },
    @{ Name = "NTM";            Repo = "Dicklesworthstone/named_tmux_manager";            API = "ntm --version" },
    @{ Name = "Agent Mail";     Repo = "Dicklesworthstone/mcp_agent_mail";                API = "am --version" },
    @{ Name = "ACFS";           Repo = "Dicklesworthstone/agentic_coding_flywheel_setup"; API = "(shell script)" }
)

foreach ($c in $checks) {
    Write-Host "-- $($c.Name) --" -ForegroundColor Magenta
    Write-Host "   Repo: https://github.com/$($c.Repo)"
    Write-Host "   API:  $($c.API)"
    Write-Host "   [ ] Проверено"
    Write-Host ""
}

Write-Host "После проверки обновите docs/INTERFACES.md" -ForegroundColor Yellow
