#!/usr/bin/env pwsh
<#
.SYNOPSIS
    Results Archive Management Tool
    Gerencia files de resultados do Training 12 Meses

.DESCRIPTION
    Permite mover, copiar e recuperar arquivos de resultados mantendo rastreamento de origem

.EXAMPLE
    .\manage_results_archive.ps1 -Action "copy" -Category "federated_learning"
    .\manage_results_archive.ps1 -Action "restore" -Category "optimization" -SubCategory "nsga2"
    .\manage_results_archive.ps1 -Action "list" -Category "all"

.NOTES
    Archive Root: c:\Users\joaop\Downloads\FAPESP\Training_12Meses\results_archive
#>

param(
    [ValidateSet("copy", "move", "restore", "list", "verify")]
    [string]$Action = "list",
    
    [ValidateSet("federated_learning", "optimization", "piml", "datasets", "research_papers", "all")]
    [string]$Category = "all",
    
    [ValidateSet("nsga2", "constrained", "sensitivity", "experiments")]
    [string]$SubCategory = "",
    
    [switch]$Force,
    [switch]$Verbose
)

# Configurações
$WorkspaceRoot = "C:\Users\joaop\Downloads\FAPESP\Training_12Meses"
$ArchiveRoot = "$WorkspaceRoot\results_archive"
$ScienceAIRoot = "$WorkspaceRoot\Science AI Engineering"

# Definições de origem para cada categoria
$SourceMappings = @{
    "federated_learning" = @{
        origin = "$ScienceAIRoot\mes10_federated_learning"
        archive = "$ArchiveRoot\federated_learning"
        patterns = @("federated_*.*", "demo_output.txt", "hybrid_demo.txt")
    }
    "optimization_nsga2" = @{
        origin = "$ScienceAIRoot\mes8_optimization\results\nsga2"
        archive = "$ArchiveRoot\optimization\nsga2"
        patterns = @("*.*")
    }
    "optimization_constrained" = @{
        origin = "$ScienceAIRoot\mes8_optimization\results\constrained"
        archive = "$ArchiveRoot\optimization\constrained"
        patterns = @("*.*")
    }
    "optimization_sensitivity" = @{
        origin = "$ScienceAIRoot\mes8_optimization\results\sensitivity"
        archive = "$ArchiveRoot\optimization\sensitivity"
        patterns = @("*.*")
    }
    "piml" = @{
        origin = "$ScienceAIRoot\mes4_piml\models"
        archive = "$ArchiveRoot\piml"
        patterns = @("*.pkl", "*.h5", "*.pt")
    }
    "datasets" = @{
        origin = "$WorkspaceRoot\Projeto\Tropical Climate Datasets"
        archive = "$ArchiveRoot\datasets"
        patterns = @("*.csv", "*.txt")
    }
    "research_papers" = @{
        origin = "$WorkspaceRoot\Projeto\Deep Search Report"
        archive = "$ArchiveRoot\research_papers"
        patterns = @("*.pdf")
    }
}

function Get-ArchiveStats {
    Write-Host "`n📊 Archive Statistics" -ForegroundColor Cyan
    Write-Host "=" * 50
    
    foreach ($category in @("federated_learning", "optimization", "piml", "datasets", "research_papers")) {
        $path = "$ArchiveRoot\$category"
        if (Test-Path $path) {
            $files = Get-ChildItem $path -Recurse -File
            $size = ($files | Measure-Object -Property Length -Sum).Sum / 1MB
            Write-Host "$category`: $(($files | Measure-Object).Count) arquivos, $([math]::Round($size, 2)) MB"
        }
    }
    Write-Host "=" * 50 "`n"
}

function List-Archives {
    param(
        [string]$Category = "all"
    )
    
    Write-Host "`n📂 Results Archive Directory" -ForegroundColor Cyan
    Write-Host "=" * 50
    
    if ($Category -eq "all") {
        Get-ChildItem $ArchiveRoot -Directory | ForEach-Object {
            Write-Host "`n📁 $($_.Name)" -ForegroundColor Yellow
            Get-ChildItem $_.FullName -Recurse -File | ForEach-Object {
                $size = "{0:N2} KB" -f ($_.Length / 1KB)
                Write-Host "   └─ $($_.Name) ($size)"
            }
        }
    } else {
        $path = "$ArchiveRoot\$Category"
        if (Test-Path $path) {
            Write-Host "`n📁 $Category" -ForegroundColor Yellow
            Get-ChildItem $path -Recurse -File | ForEach-Object {
                $size = "{0:N2} KB" -f ($_.Length / 1KB)
                Write-Host "   └─ $($_.Name) ($size)"
            }
        } else {
            Write-Host "❌ Categoria não encontrada: $Category" -ForegroundColor Red
        }
    }
    
    Get-ArchiveStats
}

function Copy-ToArchive {
    param(
        [string]$Category,
        [switch]$Recurse
    )
    
    $mapping = $SourceMappings[$Category]
    if (!$mapping) {
        Write-Host "❌ Categoria inválida: $Category" -ForegroundColor Red
        return
    }
    
    if (!(Test-Path $mapping.origin)) {
        Write-Host "⚠️  Origem não encontrada: $($mapping.origin)" -ForegroundColor Yellow
        return
    }
    
    Write-Host "`n📥 Copiando $Category para archive..." -ForegroundColor Green
    
    foreach ($pattern in $mapping.patterns) {
        $files = Get-ChildItem "$($mapping.origin)\$pattern" -ErrorAction SilentlyContinue
        if ($files) {
            Copy-Item $files -Destination $mapping.archive -Force -Recurse
            Write-Host "   ✓ Copiados: $($files.Count) arquivo(s)" -ForegroundColor Green
        }
    }
    
    Write-Host "✅ Cópia concluída para: $($mapping.archive)`n" -ForegroundColor Green
}

function Restore-FromArchive {
    param(
        [string]$Category,
        [switch]$Move
    )
    
    $mapping = $SourceMappings[$Category]
    if (!$mapping) {
        Write-Host "❌ Categoria inválida: $Category" -ForegroundColor Red
        return
    }
    
    if (!(Test-Path $mapping.archive)) {
        Write-Host "⚠️  Archive não encontrado: $($mapping.archive)" -ForegroundColor Yellow
        return
    }
    
    $action = if ($Move) { "Movendo" } else { "Copiando" }
    Write-Host "`n📤 $action $Category do archive..." -ForegroundColor Green
    
    if ($Move) {
        Move-Item "$($mapping.archive)\*" -Destination $mapping.origin -Force
    } else {
        Copy-Item "$($mapping.archive)\*" -Destination $mapping.origin -Force -Recurse
    }
    
    Write-Host "✅ Restauração concluída`n" -ForegroundColor Green
}

function Verify-Archive {
    Write-Host "`n🔍 Verificando integridade do archive..." -ForegroundColor Cyan
    
    $allFiles = Get-ChildItem $ArchiveRoot -Recurse -File
    $corruptedCount = 0
    
    foreach ($file in $allFiles) {
        if ($file.Length -eq 0) {
            Write-Host "⚠️  Arquivo vazio: $($file.FullName)" -ForegroundColor Yellow
            $corruptedCount++
        }
    }
    
    if ($corruptedCount -eq 0) {
        Write-Host "✅ Archive verificado: Todos os $($allFiles.Count) arquivos estão OK`n" -ForegroundColor Green
    } else {
        Write-Host "⚠️  Encontrados $corruptedCount arquivo(s) potencialmente corrompidos`n" -ForegroundColor Yellow
    }
}

# Main execution
switch ($Action) {
    "list" {
        List-Archives -Category $Category
    }
    "copy" {
        if ($Category -eq "all") {
            foreach ($cat in $SourceMappings.Keys) {
                if ($cat -notmatch "_") {
                    Copy-ToArchive -Category $cat
                }
            }
        } else {
            Copy-ToArchive -Category $Category
        }
    }
    "move" {
        if ($Category -eq "all") {
            Write-Host "❌ Move requer uma categoria específica (não suporta 'all')" -ForegroundColor Red
        } else {
            Restore-FromArchive -Category $Category -Move
        }
    }
    "restore" {
        if ($Category -eq "all") {
            foreach ($cat in $SourceMappings.Keys) {
                if ($cat -notmatch "_") {
                    Restore-FromArchive -Category $cat
                }
            }
        } else {
            Restore-FromArchive -Category $Category
        }
    }
    "verify" {
        Verify-Archive
    }
}

# Exibir resumo final
if ($Verbose) {
    Get-ArchiveStats
}
