$scriptPath = "C:\Users\Eliezer\Documents\DEV\PYTHON\cospe_video\main.py"

$action = New-ScheduledTaskAction -Execute 'python' -Argument "`"$scriptPath`""
$trigger1 = New-ScheduledTaskTrigger -Daily -At 11:06AM

Register-ScheduledTask -TaskName "executor-cuspidor-bot" -Action $action -Trigger @($trigger1) -Description "Roda cuspidor de video promocional"
