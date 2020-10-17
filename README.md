# CMU Interactive Data Science Assigment 3

* **Team members**: XXXX and XXXX
* **Online URL**: https://s4a.streamlit.io/cmu-ids-2020/a3-template/master/streamlit_app.py/+/

## Instructions

### Run Locally

Check out the Streamlit [getting started](https://docs.streamlit.io/en/stable/getting_started.html) guide and setup your Python environment.

To run the application locally, install the dependencies with `pip install -r requirements.txt` (or another preferred method to install the dependencies listed in `requirements.txt`). Then run `streamlit run streamlit_app.py`.

### View Online

Before you can view your application online, you need to have it set up with Streamlit Sharing. To do this, create an issue that asks the TAs to deploy your repo. To create the issue, you can follow [this link](../../issues/new?body=Dear+TAs%2C+please+add+our+repo+to+Streamlit+sharing+and+then+respond+to+this+issue+with+the+URL+to+the+deployed+application.&title=Setup+Streamlit+sharing&assignees=aditya5558,kunalkhadilkar,erbmoth) They will respond with a URL for your application. Once the repo is set up, please update the URL as the top of this readme and add the URL as the website for this GitHub repository.

### Deliverables

- [ ] An interactive data science or machine learning application using Streamlit.
- [ ] The URL at the top of this readme needs to point to your application online. It should also list the names of the team members.
- [ ] A write-up that describes the goals of your application, justifies design decisions, and gives an overview of your development process. Use the `writeup.md` file in this repository. You may add more sections to the document than the template has right now.


### How to use Git

README.md: Update for documentation
.gitignore: Add any files that you want to ignore locally

git status: Check the current status

1. Fix the file
2. git add
3. git commit
4. git push

### Data Description (new ones)
* business.csv
    * `garage`, `street`, `validated`, `lot`, `valet`: Boolean parking information
    * `dj`, `background_music`, `no_music`, `jukebox`, `live`, `video`, `karaoke`: Boolean music information (whethey business uses these musics)
    * `dessert`, `latenight`, `lunch`, `dinner`, `brunch`, `breakfast`: Type of food the restaurant is appropriate for
* review.csv
   * I used (Vader)[https://github.com/cjhutto/vaderSentiment] and converted`text` column into four additional (one being the highest and zero being the lowest):
   * `neg`: negative sentiment 
   * `pos`: positive sentiment
   * `neu`: neutral sentiment
   * `compound`: compound sentiment (normalized aggregate sentiment)


###
