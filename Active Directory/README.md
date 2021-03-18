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
***

# Privilege Escalation

### Evil Winrm:
https://github.com/Hackplayers/evil-winrm

***

# Post-Exploitation
### Bloodhound

Is a graphical interface that allows you to visually map out the network. This tool along with SharpHound which similar to PowerView takes the user, groups, trusts etc. of the network and collects them into .json files to be used inside of Bloodhound.

#### Installation

1.) ```$ apt-get install bloodhound```    

2.) ```$ neo4j console - default credentials -> neo4j:neo4j```

#### Mapping the network w/ BloodHound -

1.)```$ bloodhound``` Run this on your attacker machine not the victim machine

2.) Sign In using the same credentials you set with Neo4j
