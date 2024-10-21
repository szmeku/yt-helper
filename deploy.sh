#!/usr/bin/bash

cd ~/projects
rm -rf yt_helper_deploy
git clone yt_helper yt_helper_deploy
rm -rf yt_helper_deploy/.git
scp -i ~/.ssh/zonki-aws.pem -r yt_helper_deploy ec2-user@44.206.246.12:~/app