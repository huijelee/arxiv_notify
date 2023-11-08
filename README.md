# Environment
```conda create -n arxiv python=3.10```
```conda activate arxiv```
```pip install -r requirements.txt```

# How to set credential account and key file
```python encrypt_account.py```

\>> your email: _

\>> your password: _

The encrypted account profile is saved in data/.

# New arxiv papers to be notified
```python main.py --query "sign language" --num_paper 10```


# Daily notification
1. ```arxiv_notify_script.sh```

    Fill the conda environment and project directory
  
2.  ```crontab -e```

    Add the line: 0 7 * * * <project_dir>/arxiv_notify/main_script.sh >> <project_dir>/arxiv_notify/cron.log 2>&1
