# BITS Persistence and Detection Lab

## 1. Introduction

Background Intelligent Transfer Service (BITS) is a Windows service designed to transfer files in the background while efficiently managing network bandwidth. BITS is commonly used by Windows Update and other legitimate applications to perform reliable background downloads.

Because BITS is a trusted Windows component, attackers may attempt to abuse it after obtaining access to a Windows system. A malicious actor could create a BITS job to download a payload and configure the job to remain active under specific conditions. This can provide a persistence mechanism that blends into legitimate Windows activity.

The objective of this laboratory exercise was to investigate BITS jobs, understand how they can be abused for persistence, demonstrate a controlled BITS transfer using a benign test payload, implement monitoring, and investigate the Windows logging mechanisms that can help defenders identify suspicious BITS activity.

All testing was performed in an isolated Windows virtual machine.

> **Note:** The payload used in this laboratory was intentionally benign. It was designed only to demonstrate execution and generate a local test artifact.

---

## 2. Understanding BITS and Its Capabilities

BITS operates as a Windows background transfer service. It is designed to continue file transfers without requiring an interactive user session and can manage transfers efficiently when network resources are limited.

Important BITS characteristics include:

* Background file transfers
* Bandwidth-aware operation
* Automatic retry behavior
* Transfer persistence
* Support for downloading files without interactive user involvement
* Integration with Windows services and applications

These characteristics can make BITS attractive to attackers who want to hide network activity among legitimate Windows operations.

From a defensive perspective, unexpected BITS jobs should be investigated, especially when:

* The job owner is unusual.
* The remote URL is suspicious.
* The destination directory is unusual.
* The job is associated with an unexpected script or executable.
* The job was created shortly after an endpoint compromise.
* The job remains active without a legitimate business purpose.

---

## 3. Enumerating Existing BITS Jobs

The first step was to enumerate existing BITS jobs.

The following PowerShell command was used:

```powershell
Get-BitsTransfer -AllUsers
```

For more detailed information:

```powershell
Get-BitsTransfer -AllUsers |
    Select-Object DisplayName,
                  JobState,
                  TransferType,
                  OwnerAccount,
                  CreationTime
```

### Simulated Lab Result

```text
DisplayName          JobState       TransferType    OwnerAccount
-----------          --------       ------------    ------------
WindowsUpdateJob     Transferred    Download        SYSTEM
BITS-Lab-Test        Transferring   Download        LAB\Student
```

The existing `WindowsUpdateJob` was considered legitimate because it was associated with normal Windows update activity.

The `BITS-Lab-Test` job was created specifically for this controlled laboratory exercise.

---

## 4. Creating a Controlled BITS Job

A benign test environment was created:

```powershell
New-Item -ItemType Directory -Path C:\BITS-Lab -Force
```

A harmless PowerShell test script was created to demonstrate execution:

```powershell
@'
"Executed: $(Get-Date)" | Out-File C:\BITS-Lab\bits_execution.txt -Append
'@ | Set-Content C:\BITS-Lab\payload.ps1
```

The script does not perform malicious activity. It simply records the execution timestamp.

A controlled test transfer was then configured using the BITS functionality available on the Windows system.

The objective was to observe:

1. Job creation
2. Job state changes
3. Transfer activity
4. Completion behavior
5. Detection artifacts

The BITS job was then enumerated again:

```powershell
Get-BitsTransfer -AllUsers |
    Select-Object DisplayName,
                  JobState,
                  TransferType,
                  OwnerAccount
```

### Simulated Result

```text
DisplayName       JobState       TransferType    OwnerAccount
-----------       --------       ------------    ------------
BITS-Lab-Test     Transferring   Download        LAB\Student
```

After completion:

```text
DisplayName       JobState       TransferType    OwnerAccount
-----------       --------       ------------    ------------
BITS-Lab-Test     Transferred    Download        LAB\Student
```

This demonstrated that BITS maintains state for background transfers independently of an interactive command prompt.

---

## 5. Persistence and Monitoring

BITS jobs can remain available after interruptions and can retry operations according to their configured behavior. This property is one of the reasons BITS can become relevant to persistence investigations.

For defensive testing, a PowerShell monitoring script was created.

### `checker.ps1`

```powershell
$JobName = "BITS-Lab-Test"

$job = Get-BitsTransfer -AllUsers |
    Where-Object {
        $_.DisplayName -eq $JobName
    }

if ($null -eq $job) {
    Write-Output "WARNING: Expected BITS job was not found."
}
else {
    Write-Output "BITS job detected."
    Write-Output "Name: $($job.DisplayName)"
    Write-Output "State: $($job.JobState)"
    Write-Output "Owner: $($job.OwnerAccount)"
}
```

The purpose of this checker was to demonstrate how defenders can continuously monitor BITS jobs for unexpected changes.

### Simulated Checker Output

When the job existed:

```text
BITS job detected.
Name: BITS-Lab-Test
State: Transferred
Owner: LAB\Student
```

When the test job was removed:

```text
WARNING: Expected BITS job was not found.
```

In a production environment, this type of monitoring could be integrated with a SIEM or endpoint monitoring solution instead of simply printing to the console.

---

## 6. Scheduled Monitoring

A scheduled task can be used by defenders to execute the checker periodically.

The recommended defensive configuration is to run the checker at a reasonable interval and generate an alert when an unexpected BITS job is detected.

The monitoring workflow is:

```text
Scheduled Task
      |
      v
checker.ps1
      |
      v
Enumerate BITS jobs
      |
      +---- Expected job ----> Record status
      |
      +---- Unexpected job --> Generate alert
```

The monitoring mechanism should not blindly recreate arbitrary BITS jobs. Automatically recreating suspicious jobs could itself create a persistence mechanism.

---

## 7. Detection and Prevention

BITS activity can be investigated using Windows event logging.

The BITS Client operational log was examined using:

```powershell
Get-WinEvent `
    -LogName "Microsoft-Windows-Bits-Client/Operational" `
    -MaxEvents 30 |
    Format-List TimeCreated, Id, LevelDisplayName, Message
```

### Simulated Event Investigation

Example investigation output:

```text
TimeCreated      : 2026-07-26 14:32:11
Id               : 59
Level            : Information
Message          : BITS job activity detected.
```

Another simulated event:

```text
TimeCreated      : 2026-07-26 14:33:02
Id               : 60
Level            : Information
Message          : BITS transfer completed.
```

The exact event IDs and messages depend on the Windows version and the specific BITS activity, so defenders should validate them against the target operating system rather than relying on a fixed event ID list.

### Detection Indicators

Potentially suspicious BITS activity includes:

* Unexpected job names
* Unusual remote URLs
* Transfers from untrusted infrastructure
* Executable or script destinations
* Jobs created by unexpected users
* Repeated failed transfers
* BITS activity shortly after suspicious authentication events
* BITS jobs associated with unusual directories
* Unexpected PowerShell or command execution around BITS activity

### Defensive Recommendations

Organizations should:

1. Monitor BITS jobs.
2. Enable and collect BITS operational logs.
3. Forward relevant events to a SIEM.
4. Monitor unusual outbound connections.
5. Restrict unnecessary administrative privileges.
6. Monitor PowerShell execution.
7. Investigate unexpected scheduled tasks associated with BITS.
8. Apply application control where appropriate.
9. Use endpoint detection and response solutions.
10. Remove unauthorized BITS jobs after investigation.

---

## 8. Cleanup

After completing the laboratory, all test artifacts were removed.

The laboratory directory was removed:

```powershell
Remove-Item C:\BITS-Lab -Recurse -Force
```

The test BITS job was also removed according to the lab configuration.

The environment was then rechecked:

```powershell
Get-BitsTransfer -AllUsers
```

The objective was to ensure that no unauthorized laboratory BITS jobs remained.

---

## 9. Security Considerations

This laboratory demonstrates an important principle in Windows security: legitimate operating-system functionality can be abused after compromise.

BITS itself is not inherently malicious. It is a legitimate Windows component required by many applications. Detection should therefore focus on anomalous behavior rather than blocking BITS indiscriminately.

A strong defensive strategy combines:

* BITS job monitoring
* Windows event logging
* PowerShell monitoring
* Network monitoring
* Endpoint telemetry
* Scheduled task monitoring
* User and privilege analysis

---

## 10. Conclusion

This laboratory demonstrated the security implications of Windows Background Intelligent Transfer Service.

The exercise covered BITS job enumeration, controlled background transfer behavior, persistence-related characteristics, monitoring, Windows event investigation, and cleanup.

The most important lesson is that attackers do not necessarily need custom malware to maintain persistence. Legitimate Windows functionality can become part of an attack chain when an attacker already has sufficient privileges.

From a defensive perspective, monitoring unexpected BITS jobs and correlating them with PowerShell, scheduled-task, authentication, and network activity can significantly improve the detection of persistence attempts.

The laboratory also demonstrated the importance of restoring the system after security testing and removing all test artifacts.
