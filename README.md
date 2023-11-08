# how to get credential account and key file
>> python encrypt_account.py

# new arxiv papers to be notified
>> python main.py

# get notification every day
1. set arxiv_notify_script.sh
>> crontab -e
>> 0 7 * * * <project_dir>/arxiv_notify/main_script.sh >> <project_dir>/arxiv_notify/cron.log 2>&1
