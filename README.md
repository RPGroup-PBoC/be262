# Webpage for `BE262`, Physical Biology Bootcamp at Caltech
### Rob Phillips Group
### https://www.rpgroup.caltech.edu/be262/

## How to update/archive website material
Say we're in year 20XX. To make a new year's offering course webpage for the new year 20XX+1:
1. First, archive the current/old year's `index.html` page. Do this by making a new directory called the current year, '20XX', and copying the current `index.html` file held at the top level of this `be262` directory into the new directory. (The logic of the whole webpage is that whatever `index.html` is found at the top level is the one served by github pages to visitors to the webpage without a year suffix.)
2. Next, edit the `index.html` file still at the top level of `be262` to indicate the new year, by changing `year: 20XX` to `year: 20XX+1`. 
3. Now, go to the `_posts` directory. This directory contains the majority of files you would be updating the content of that comprise the website (eg those `About`, `People`, `Programming`, and `Readings` links that populate the left side of the webpage). The webpage framework essentially expects a structure like a blog, so each of the Markdown files in `_posts` contains a date. These dates are arbitrary, except for the fact that the current year's posts must all have the current numerical year correctly specified. So, copy the old/current year's posts---namely, eg `20XX-01-24-readings.md`, `20XX-01-25-code.md`, and so on---into new versions that are renamed with the new year, e.g. `20XX+1-01-24-readings.md`, etc. Next, inside each of these year `20XX+1` post .md files, edit anything that says the old `20XX` year into `20XX+1`: e.g. at the minimum the `tag:` and `year:` attributes at the top of each of the files. But also, for e.g. the `20XX+1-01-24-code.md` file, you'll need to edit a mention in `site.data.20XX.speakers` to `site.data.20XX+1.speakers`, etc. 
4. That last edit recommends that under `_data`, there will be expected to be a directory with each year where info is to be found. So, cd into `_data` and copy the old year `20XX` directory into a new directory named `20XX+1`. 
5. Edit these `_data/20XX+1` files accordingly to reflect the new schedule of speakers, the new TA's, any mugshots, etc. Add any new people/speaker mugshots to `be262/images/people/` so you can call them in files found in `_data/20XX+1`; remember that it is strongly recommended that all images are square in aspect ratio to prevent formatting weirdness.
6. Update anything else with new materials! Remember to commit etc.

