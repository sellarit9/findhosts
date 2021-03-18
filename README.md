Utilzing nmap (https://nmap.org/) to determine what hosts exists in a subnet. Then pushing data to Datadog to track and visualize. 

**Requirements: (All testing as of March 18, 2021 was done on a macOS Catalina 10.15.7)**
1. nmap installed on a host machine - https://nmap.org/download.html
2. python3
3. python libraries:
    - python-nmap
    - json
    - os
    - requests
    - yaml
    - random
    - time
    - json

4. Datadog agent on host machine
    - apm enabled
    - logging enabled
    - Configure datadog.yaml 
      - apm_config: env: hosts (or whatever you want, this will be the Service Map scope)
  


**config.yaml**

This is where you will set what subnets you wish to scan for hosts


**findHosts.py**

Script that runs nmap scan.
At top, set your DD_CLIENT_API_KEY



**In Datadog UI**

You will see logs idexed, which come in as JSON, and from there you can created your facets.
You will also see traces created and in time see the service map created (under the env you setup in the datadog yaml under apm_config)
