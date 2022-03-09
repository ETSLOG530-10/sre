import json
from pip._vendor import requests
import csv
import traceback

def request_get(url, token):
    res = requests.get(url, headers={"Authorization": f"token {token}", 'Cache-Control': 'no-cache', 'Pragma': 'no-cache'})
    if res.status_code >= 400:
        raise Exception('Limit exeded')
    return res

code_exts = [".kt", ".java", ".cpp", ".h", ".js", ".scss", ".css"] # Could have more exts.
def is_code_file(filename):
    for code_ext in code_exts:
        if filename.endswith(code_ext):
            return True
    return False


# @commitlist empty list, fof commits
# @lstTokens GitHub authentication tokens
def countfiles(commitlist, lsttokens, repo):
    ipage = 1  # url page counter
    ct = 0  # token counter
    try:
        # loop though all the commit pages until the last returned empty page
        while True:
            ok_1 = False
            while not ok_1:
                try:
                    if ct == len(lstTokens):
                        ct = 0
                    spage = str(ipage)
                    # commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + \
                    #              '&per_page=100&access_token=' + lsttokens[ct]
                    commitsUrl = 'https://api.github.com/repos/' + repo + '/commits?page=' + spage + \
                                '&per_page=100'
                    content = request_get(commitsUrl, lsttokens[ct])
                    ct += 1
                    jsonCommits = json.loads(content.content)
                    print(content.content)
                    # break out of the while loop if there are no more commits in the pages
                    if len(jsonCommits) == 0:
                        return
                    ok_1 = True
                except:
                    input("1" + traceback.format_exc())
                    ct += 1
            # iterate through the list of commits in a page
            commitNumber = 100*ipage
            for shaObject in jsonCommits:
                ok_2 = False
                while not ok_2:
                    try:
                        sha = shaObject['sha']
                        if ct == len(lstTokens):
                            ct = 0
                        # For each commit, use the GitHub commit API to extract the files touched by the commit
                        # shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha \
                        #          + '?access_token=' + lstTokens[ct]
                        shaUrl = 'https://api.github.com/repos/' + repo + '/commits/' + sha
                        content = request_get(shaUrl, lstTokens[ct])
                        ct += 1
                        shaDetails = json.loads(content.content)

                        commitlist.append(json.loads(content.content.decode("utf-8")))
                        print(f"Commit page = {spage} ; Commit number = {commitNumber}")
                        print(content.content)
                        ok_2 = True
                    except:
                        input("2" + traceback.format_exc())
                        ct += 1
                    # filesjson = shaDetails['files']
                    # for filenameObj in filesjson:
                    #     filename = filenameObj['filename']
                    #     print(filename)
                    #     # writer.writerow(rows)
                    #     dictfiles[filename] = dictfiles.get(filename, 0) + 1
                commitNumber+=1
            ipage += 1
    except Exception as e:
        input("3" + traceback.format_exc())
        json.dump(commitlist, fileOutputCommitsJSON)
        exit(0)

# repo = 'scottyab/rootbeer' # (Tous les fichiers)
# repo = 'Skyscanner/backpack' # (uniquement les fichiers source)
# repo = 'k9mail/k-9' # (uniquement les fichiers source)
# repo = 'mendhak/gpslogger'

# put your tokens here
lstTokens = ['']

def get_github_data(repo):
    file = repo.split('/')[1]
    fileOutputCommitsJSON = open(file + ".json", 'w')
    # dictfiles = dict()
    commitlist = []
    countfiles(commitlist, lstTokens, repo)
    json.dump(commitlist, fileOutputCommitsJSON)
    fileOutputCommitsJSON.close()
    return file + ".json"

def main():
    repo = input("Repo: ")
    filename = get_github_data(repo)


if __name__ == "__main__":
    main()