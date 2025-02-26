# LLM's decision making under uncertainty

Simple overview of use/purpose.

## Description

An in-depth paragraph about your project and overview of use.


## ✅ TODO List
Current Game: Lottery Choices
Proprity:
- [ ] Choose multiple models, but one at a time
     - [x] gpt-3.5-turbo             #is_chat       is_api       is_supported_fc    
     - [x] gpt-3.5-turbo-instruct    #is_chat F     is_api       is_supported_fc F
     - [x] gpt-4-turbo               #is_chat       is_api       is_supported_fc
     - [x] gpt-4o                    #is_chat       is_api       is_supported_fc
     - [ ] llama2-7b 
     - [ ] llama2-13b
     - [ ] llama2-70b
     - [ ] vicuna-7b
     - [ ] vicuna-13b
     - [ ] vicuna-33b
     Note: need to include? 
     - [ ] llama3
     - [ ] deepseek
- [ ] How to write testing so that i don't have to keep writing test everytime i change something
- [ ] See previous response vs not previous response
- [ ] Extract final output whether or not model chooses A or B  #probability probing?
     - [x] function_calls for applicable models # not long-term solutions because some models not applicable
     - [ ] write alternative methods for other non-fc models openai -> regex 
     - [x] write alternative methods for other non-fc models openai -> another models to extract. 
     - [x] write alternative methods for llama and vicuna --> another models to extract should work too for now
- [ ] for some reason the output is super long hence the reasoning is not finished, and so no final option can be concluded
- [ ] Make an alternative for BDI for function call >> must also change function_schema
- [ ] Search for a better BDI reasoning
- [ ] Record the r point (choosing between OptionA or OptionB)
- [ ] Analysis

### 🔹 Completed Tasks ✅
- [x] Initialized project - setup docker
- [x] Set up simple lottery choices
     - [x] one model working
     - [x] able to choose one prompt type
     - [x] able to execute one round of game
- [x] Created initial documentation
- [x] Make it run multiple round all round
- [x] Record the results 
- [x] Think of the BDI model
- [x] Add logging for debug purpose
      - [x] Create logging_config.py
      - [x] Output to log as well as terminal
- [x] Test logging
- [x] Create a config.yml file 
- [x] Make testing without function without incurring LLM cost
- [x] How to handle cases where we cannot extract options --> returns None 
- [x] Make reasoning more dynamic, can support if new reasoning approach is introduced --> see agent/reasoning.py
- [x] Make function call more modula

### 🔹 Note to self:
- Currently the model seems to be overly rational! it starts to calculating EV! huamn don't do that
- Model choose each row idependently, it shouldn't it should see previous selected choice
- Can we use free API for llama2


## Getting Started

### Dependencies

* Describe any prerequisites, libraries, OS version, etc., needed before installing program.
* ex. Windows 10

### Installing

* How/where to download your program
* Any modifications needed to be made to files/folders

### Executing program

* How to run the program
* Step-by-step bullets
```
docker-compose up --build -d
```

## Help

Any advise for common problems or issues.
```
command to run if program contains helper info
```

## Authors

Contributors names and contact info

ex. Dominique Pizzie  
ex. [@DomPizzie](https://twitter.com/dompizzie)

## Version History

* 0.2
    * Various bug fixes and optimizations
    * See [commit change]() or See [release history]()
* 0.1
    * Initial Release

## License

This project is licensed under the [NAME HERE] License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* The codebase is adapted from Agent-trust (paper) which is under this license. Thanks for the amazing work! (https://github.com/camel-ai/agent-trust)
<!-- * [awesome-readme](https://github.com/matiassingers/awesome-readme)
* [PurpleBooth](https://gist.github.com/PurpleBooth/109311bb0361f32d87a2)
* [dbader](https://github.com/dbader/readme-template)
* [zenorocha](https://gist.github.com/zenorocha/4526327)
* [fvcproductions](https://gist.github.com/fvcproductions/1bfc2d4aecb01a834b46) -->
<!-- docker-compose up --build -d
docker-compose down -->
