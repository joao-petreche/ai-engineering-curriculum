@echo off
REM Helper script to test local Kubernetes deployment (Windows)
REM Usage: test-k8s.bat [dev|staging|prod]

setlocal enabledelayedexpansion

set ENVIRONMENT=%1
if "%ENVIRONMENT%"=="" set ENVIRONMENT=dev

set NAMESPACE=bps-%ENVIRONMENT%

echo Testing Kubernetes deployment for: %NAMESPACE%

REM Check if namespace exists
kubectl get namespace "%NAMESPACE%" >nul 2>&1
if errorlevel 1 (
    echo ❌ Namespace %NAMESPACE% does not exist
    exit /b 1
)

echo ✅ Namespace %NAMESPACE% exists

REM Check pods
echo.
echo Checking pods...
kubectl get pods -n "%NAMESPACE%" --no-headers | findstr "Running" >nul 2>&1
if errorlevel 1 (
    echo ❌ No running pods found
    exit /b 1
)

echo ✅ Running pods found:
kubectl get pods -n "%NAMESPACE%" -o wide

REM Check services
echo.
echo Checking services...
kubectl get svc -n "%NAMESPACE%"

REM Port-forward and test health
echo.
echo Testing health endpoint...
start /b kubectl port-forward -n "%NAMESPACE%" svc/bps-api 8000:8000
timeout /t 3 /nobreak >nul

curl -f http://localhost:8000/health >nul 2>&1
if errorlevel 1 (
    echo ❌ Health endpoint failed
    taskkill /f /im kubectl.exe >nul 2>&1
    exit /b 1
)

echo ✅ Health endpoint responsive

curl -f http://localhost:8000/health/ready >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Readiness check failed (dependencies may not be ready)
) else (
    echo ✅ Readiness check passed
)

taskkill /f /im kubectl.exe >nul 2>&1

echo.
echo ✅ All tests passed for %NAMESPACE%
