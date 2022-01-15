Fix "Permission Denied" Error From Github

Random Github permission errors are the worst!

You're probably familiar with this error:


Screenshot of terminal code trying to clone a private repository from Github and getting Permission denied (public key) error in response

Showing "Permission denied" error in the terminal

You don't know where it comes from. It's frustrating, and you want to get on with deploying and working on your project. The things that actually matter.



Let's investigate a few possible reasons for why you're seeing this error and a solution for each one of them. 👇🏼



Read on or if you prefer video, watch it below.


Play

🔗Don't use sudo with git 🙅🏻‍♀️

First of all, try not to use sudo command with git. When you use sudo, you're running the command as the root user and SSH will use a different key pair to authenticate with Github.



When you generate SSH keys without sudo and then use sudo to clone a repository, you won't be using the same keys you generated. This leads to Github denying access to your private repositories because it can't verify that it's you.



If you're on a VPS and logged in as root, using sudo doesn't make a difference so this is probably not the reason for the error. However, using root is generally considered insecure and it's better to create a non-root user and disable root login altogether.



🔗Avoid typos by copying the repository location 📋

If you're cloning a repository, double-check you didn't make any typos in the command. It's easy to omit or misspell a letter without you noticing. The correct format for cloning a Github repository using SSH is:



# Syntax for cloning a Github repository using SSH

git clone git@github.com:[username]/[repository].git

I recommend copying the repository location from the Github website to avoid making manual mistakes. You can do this by navigating to the repository page and look for a green button labelled "Code" in the upper right corner.



The "Code" button in the upper-right corner expands to a menu that lets you copy the repository clone command with a push of a button

Screenshot of Github repository page showing copy command button

In case you're trying to push to Github, make sure the remote is spelled correctly and pointing to the right repository. You can view a repository's remotes with:



# View a repository's remote list

git remote -v

🔗Make sure you have a key pair and that the SSH client is using it 🔑

Next troubleshooting step is to check whether the SSH client can find a private key to authenticate with Github.



To debug an SSH connection you can pass the -v flag to the SSH command. Therefore, to debug your SSH connection with Github, you would type:



# Debug the SSH connection to github.com

ssh -v git@github.com

This will print out a few things to the terminal. Look out for a sequence of lines starting with debug1: identity file .... This is the SSH client trying to find a private key by going through a list of possible filenames. In my case, the debug output looks as follows:



debug1: Connecting to github.com port 22.

debug1: Connection established.

debug1: identity file /Users/maxim/.ssh/id_rsa type 0

debug1: identity file /Users/maxim/.ssh/id_rsa-cert type -1

debug1: identity file /Users/maxim/.ssh/id_dsa type -1

debug1: identity file /Users/maxim/.ssh/id_dsa-cert type -1

debug1: identity file /Users/maxim/.ssh/id_ecdsa type -1

debug1: identity file /Users/maxim/.ssh/id_ecdsa-cert type -1

debug1: identity file /Users/maxim/.ssh/id_ed25519 type -1

debug1: identity file /Users/maxim/.ssh/id_ed25519-cert type -1

debug1: identity file /Users/maxim/.ssh/id_xmss type -1

debug1: identity file /Users/maxim/.ssh/id_xmss-cert type -1

The -1 at the end of each line stands for not found. As you can see, SSH was able to find my private key at /Users/maxim/.ssh/id_rsa and will use it to authenticate with Github.



If you don't have a key pair, you can generate one fairly simple. Github has a good guide on how to generate an SSH key pair.



If you're trying to clone a repository from a fresh new VPS, most likely there's no private key present on the server. You can either copy an existing private key from your local machine or create a new SSH key pair on the remote server. I recommend the latter for better security.



In case you do have a key pair on the system but the SSH client cannot find it, because it's in a different location or has a different name, you have two options:



Rename and place the key in the default location ~/.ssh/id_rsa so SSH can find it

Let SSH know where to find your private key. You can do this with a oneliner:

# Authenticate with a specific key while cloning a repository

GIT_SSH_COMMAND='ssh -i /path/to/private_key -o IdentitiesOnly=yes' git clone git@github.com:[username]/[repository].git

Or you can add a ~/.ssh/config file with the following contents:



Host github.com

  IdentityFile /path/to/private_key

  IdentitiesOnly yes

Make sure the file has the correct permissions with the following command:




# Restrict write & read access to the file owner

chmod 600 ~/.ssh/config

🔗Verify that the correct public key is attached to your Github account 👀

Lastly, let's verify that the correct public key is added to your Github account.



Go to github.com, click on your avatar and then "Settings". Find the "SSH and GPG keys" section on the left side and click on it. In the right pane, you'll see a list of SSH keys associated with your account.



Settings page with a navigation bar on the left and main section showing the uploaded keys, if any

SSH and GPG keys section in Github settings

Each public key in this list grants the corresponding private key access to your repositories.



Back in your terminal, type the following:



# Print the public key's fingerprint

ssh-keygen -E md5 -lf ~/.ssh/id_rsa.pub

This will print the fingerprint of your public key. Change the path if your public key is at a different location or has a different name.



You can find the public key that corresponds to a certain private key by looking at the file names. The naming convention is to add a .pub suffix to the public key. The default private and public keys are named id_rsa and id_rsa.pub, respectively.



If you don't see a public key fingerprint in your Github account that matches the output in your terminal, you'll need to add the public key to your Github account to gain access to your repositories.



🔗Conclusion

In this article, we've looked at some possible solutions for the "Permission denied" error from Github:



Don't use sudo with git

Avoid typos by copying the repository location from the Github website

Make sure you have a key pair and that the SSH client is using it

Add the correct public key to your Github account

I hope this helped you solve this pesky error so you can continue working on your project.
