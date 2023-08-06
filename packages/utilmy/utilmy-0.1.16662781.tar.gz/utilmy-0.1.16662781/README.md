
[![Build and Test , Package PyPI](https://github.com/arita37/myutil/actions/workflows/build%20and%20release.yml/badge.svg)](https://github.com/arita37/myutil/actions/workflows/build%20and%20release.yml)

[     https://pypi.org/project/utilmy/#history ](https://pypi.org/project/utilmy/#history)



## utilnmy
    1000s of One liner function utilities.
    
    https://packagegalaxy.com/python/utilmy


    https://arita37.github.io/myutil/en/zdocs_y23487teg65f6/genindex.html


### Install for development

    https://github.com/arita37/myutil/issues/9






 # How the documentation is generated:
```

  Commit in zdocs_y23487teg65f6 branch
     --> Trigger   .github/auto_docs_githubpages.yml
           ---> Install Sphynx Doc
              -->  Launch docs_ghpage/buildDocs.sh
                    -->  Generate Doc + Push doc into gh-pages branch
                         here :   https://github.com/arita37/myutil/blob/gh-pages/en/zdocs_y23487teg65f6/index.html
                         
                      --. Every 10 mins, Github picks up the content of gh-pages branch and publish on Internet


Config files to updates:

     docs_ghpages/ builDocs.sh : Sphynx +  git push to gh-pages

    docs_ghpages/ index.rst  : template of the Index.html

    docs_ghpages/   conf.py : Sphynx generator


Doc pushed here:

    https://github.com/arita37/myutil/blob/gh-pages/en/zdocs_y23487teg65f6/index.html








```

## How to use 
 
    https://drive.google.com/drive/folders/1FawUmqrNOxabWbepiCchDd1b60pseDXm?usp=sharing
 

    VizHTML
    https://colab.research.google.com/drive/1blfkg8sFMcRmIULhJVMZ8BIC5x_2YrDl?usp=sharing

    https://colab.research.google.com/drive/12rpbgH3WYcQq3jtl9vzEYeVdu9a9GOM_?usp=sharing 
    
    https://colab.research.google.com/drive/1NYQZrfAPqbuLCt9yhVROLMRJM-RrFYWr#scrollTo=Rrho08zYe6Gj

    https://colab.research.google.com/drive/1NYQZrfAPqbuLCt9yhVROLMRJM-RrFYWr#scrollTo=2zMKv6MXOJJu


 

 ## Datasets available :
 
 https://github.com/arita37/zdata/blob/main/README.md
 



 # How the documentation is generated:

  Commit in zdocs_y23487teg65f6
     --> Trigger   .github/auto_docs_githubpages.yml
           ---> Install Sphynx Doc
              -->  Launch docs_ghpage/buildDocs.sh
                    -->  Generate Doc + Push doc into gh-pages branch
                      --. Every 10 mins, Github picks up the content of gh-pages and publish on Internet


                      

 
 
 

 #   Patching for Intel CPU speed up

        https://intel.github.io/scikit-learn-intelex/acceleration.html

        Through global patching to enable patching for your scikit-learn installation for all further runs:
        python sklearnex.glob patch_sklearn

        pip install scikit-learn-intelex
 

