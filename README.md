# duplicity-stitcher

A python script for stiching together multi-volume files when recovering a broken duplicity backup.

## The Story

I had failing memory chips which were causing random crashes on my computer.  I mistook that for a failing SSD and backed up my data, replaced the SSD, then discovered my backup was corrupt... because bad memory.

As I sought an answer, I discovered recovering duplicity backups manually is a bit involved, but possible.  

Duplicity Stitcher is the third and final step of that process, allowing you to concatenate a "multi-volume" file - a large file that's been split into smaller pieces for archival.

## Recovering a backup.

There are three key steps:

1. unzip the backupfiles (use vol_parse.sh)
2. untar the unzipped backup files to restore the directory structure (use Ark)
3. recover your lost data by stiching if necessary

I suggest recovering a small portion of a corrupted backup at a time as the process can quickly become very time consuming for a large data set.  The duplicity manifest file generated with the backup is a great way to quickly identify data files and the volume numbers under which they're stored.

### Step 1 - gzip.

Use the script `vol_parse.sh` to unzip the tar files to the same directory with `bash vol_parse.sh` .  Ignore reported errors.  The result will be tar files simply named `volxxxx` according to the volume number encoded in the original zip filename

### Step 2 - tar.

Using tar on the commandline would be ideal, but I couldn't sort out how to get it to untar corrupted files.  Instead, I installed Ark (the KDE archive tool) as it proved to be quite fault-tolerant and you can use it to batch un-tar files from a file explorer window.  Note that corrupted files will trigger a dialog asking you if you want to abort or open the file as read-only.  Obviously, pick "read-only".

Once opened, extract the files.  UNCHECK "Extraction into subfolder" and extract the folder structure to the current folder.  Also, I suggest checking "Close Ark after extraction" to save a step, especially if you end up running Ark several times for some reason (like batch conversion fails).

### Step 3 - Duplicity Stitcher.

You may not need the sticher here.  Duplicity does not split up smaller files, so check the folders under "snapshot" first for a particular file.  If the file is missing, look for a folder with the file's name under "multivol_snapshot".  That folder should contain the original file split into multiple volumes.  If this is the case, you need Duplicity Stitcher.

Run duplicity stitcher by typing `python duplicity_stitcher` (or `python3` as is the case for some) to start the GUI.

Select the multi-volume file you wish to recover by clicking the open button, then recover it by clicking the "stitch" button.  The resulting stitched file will be saved in the corresponding multivol_snapshot subfolder alongside the multi-volume files that were used for the stitch.

Note you could use the `cat` command in the terminal to achieve the same result.  However, `cat` has a maximum file limitation, which, I believe, is why this project came into existence originally.

## Credits

This code really isn't my own.  It was originally posted in 2013 on a website that no longer exists, then updated with a few bug fixes in 2016 as a github gist.  To that end, I consider it largely abandonware and have updated it again for python3 compatibility and to fix other compatibility issues.  I have also renamed the project and posted it under the MIT license.

I don't expect to need this software ever again. I imagine most everyone who ever needs it will not need it a second time, either.  As such, I'm not really going to maintain the project beyond this point - though there's plenty of room for improvement if someone is inclined to fork the project and do that.

## Links

This is the updated version of duplicity_join.py by hellocatfood.
https://gist.github.com/hellocatfood/63b04fd011233d56a09a25c2cec0c6c7

The original code base is on the archive.org Wayback Machine:
https://web.archive.org/web/20160506043217/http://blog.atoav.com/2013/09/restore-broken-deja-dup-backup-hand/

Repairing / manually extracting duplicity files:
https://askubuntu.com/questions/473124/extract-duplicity-files-manually

https://serverfault.com/questions/249709/how-to-manually-extract-a-backup-set-made-by-duplicity

Includes Python commandline code which functions similarly to Duplicity Sticher:
https://askubuntu.com/questions/1123058/extract-unencrypted-duplicity-backup-when-all-sigtar-and-most-manifest-files-are




