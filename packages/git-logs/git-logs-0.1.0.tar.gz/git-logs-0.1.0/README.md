# git-logs
> compare & filter commits based on frequency, author etc

## Contribution Guidelines
- Read  [CONTRIBUTION.md](CONTRIBUTION.md)

## Installation 
```bash
pip install git-logs

# upgrade to latest version
pip install --upgrade git-logs
```

## Usage 

> NOTE: Both git-logs and gitlogs work.

- By default commits will be listed by `month`
```bash
gitlogs -f day
```
![screenshot of the above command](https://drive.google.com/uc?export=view&id=1WQhvmRhPos022V_4rha5LHXX9HITddWp)

- `Help` options

![screenshot of help option](https://drive.google.com/uc?export=view&id=18QQCbFcesh-1q2nXc0jSWiaUz9Bu_0Z9)

- Error when `git not initialized` 

![screenshot of error](https://drive.google.com/uc?export=view&id=1KtmpoPrUdaov7GfoJ3MDf-3zNWQ63sYZ)

## To-Do
- [x] Display package version - also checks if installed or not
- [x] Add option to change the default display bar
- [x] Make date format more readable.
- [x] Automate the process of publishing package to `pypi` using `Actions`
- [x] Highlight weekends.
- [x] Fix `color` issue on Windows Powershell/CMD
- [ ] Add option to change default frequency
- [ ] Add option to list last `n` commits