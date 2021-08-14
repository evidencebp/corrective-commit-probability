"""
 curl -H "Accept: application/vnd.github.mercy-preview+json" https://api.github.com/repos/dipakkr/A-to-Z-Resources-for-Students/topics
{
  "names": [
    "hackathon",
    "students",
    "android",
    "conferences",
    "react",
    "udacity",
    "awesome-list",
    "awesome"
  ]
}
"""

from os.path import join
import requests
from github import Github
from time import sleep


from cred import GITHUB_TOKEN
from configuration import DATA_PATH
from batch_process import BatchProcessor


def get_reop_topics_link(repo_name):
    link_template = "https://api.github.com/repos/{repo_name}/topics"

    return link_template.format(repo_name=repo_name)


def get_link_content(link):
    content = requests.get(link)

    return content

def get_repo_topics(repo_name
                    , git_interface):
    #pdb.set_trace()
    r = git_interface.get_repo(repo_name)
    return r.get_topics()


#c = get_link_content(get_reop_topics_link('dipakkr/A-to-Z-Resources-for-Students'))
git_interface = Github(GITHUB_TOKEN)


def get_topics_of_repo(repo):

    return get_repo_topics(repo['repo_name']
                    , git_interface)

#import pdb; pdb.set_trace()
pause_function = lambda: sleep(10)

bp = BatchProcessor(input_file=join('/Users/idan/Downloads/'
                                    , 'reops_2020.csv')
                    , output_file=join(DATA_PATH
                                    , 'repos_2020_topics.csv')
                    , prev_file=None
                    #, prev_file=join(DATA_PATH
                    #                , 'repos_topics_agg.csv')
                    , fetch_function=get_topics_of_repo
                    , keys=['repo_name']
                    , error_file=join(DATA_PATH
                                    , 'repos_topics_errors.csv')
                    , pause_function=pause_function
                    )
bp.process()
