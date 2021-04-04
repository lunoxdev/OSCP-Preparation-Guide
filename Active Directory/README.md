# Full Guide
***

# Power shell basic commands

### PowerView-3.0-tricks.ps1
Powerview is a powerful powershell script from powershell empire that can be used for enumerating a domain after you have already gained a shell in the system.

https://gist.github.com/HarmJ0y/184f9822b195c52dd50c379ed3117993

***

# Attacking Kerberos
### Kerbrute
Kerbrute is a popular enumeration tool used to brute-force and enumerate valid active-directory users by abusing the Kerberos pre-authentication. You can discovery users, passwords and even password spray!

Installation 

1.) Download a precompiled binary for your OS - https://github.com/ropnop/kerbrute/releases

2.) Rename kerbrute_linux_amd64 to kerbrute

3.)```$ chmod +x kerbrute - make kerbrute executable```

***

### Rubeus
Is a powerful tool for attacking Kerberos. Just some of the many tools and attacks include overpass the hash, ticket requests and renewals, ticket management, ticket extraction, harvesting, pass the ticket, AS-REP Roasting, and Kerberoasting.

https://github.com/GhostPack/Rubeus


### Mimikatz
Is an open-source application that allows users to view and save authentication credentials like Kerberos tickets. Is a very popular and powerful post-exploitation tool most commonly used for dumping user credentials inside of an active directory network

https://github.com/gentilkiwi/mimikatz

#### Basic commands here: https://adsecurity.org/?page_id=1821


***

# Post-Exploitation
Post-exploitation refers to any actions taken after a session is opened. A session is an open shell from a successful exploit or bruteforce attack. A shell can be a standard shell or Meterpreter.


### Evil Winrm:

#### Privilege Escalation
In order to make life easier to system administrators, this program can be used on any Microsoft Windows Servers with this feature enabled (usually at port 5985), of course only if you have credentials and permissions to use it. So we can say that it could be used in a post-exploitation hacking/pentesting phase. The purpose of this program is to provide nice and easy-to-use features for hacking. It can be used with legitimate purposes by system administrators as well but the most of its features are focused on hacking/pentesting stuff.

https://github.com/Hackplayers/evil-winrm

### Bloodhound

Is a graphical interface that allows you to visually map out the network. This tool along with SharpHound which similar to PowerView takes the user, groups, trusts etc. of the network and collects them into .json files to be used inside of Bloodhound.

#### Installation

1.) ```$ apt-get install bloodhound```    

2.) ```$ neo4j console - default credentials -> neo4j:neo4j```

#### Mapping the network w/ BloodHound -

1.)```$ bloodhound``` Run this on your attacker machine not the victim machine

2.) Sign In using the same credentials you set with Neo4j


***
Check My work:
https://www.instagram.com/lunox.code/
***
