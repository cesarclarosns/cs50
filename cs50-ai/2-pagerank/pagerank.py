import copy
import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    # Create an empty dictionary for the probability distribuition
    prob_dist = {}
    
    # Probability of choosing a link at random chosen from all pages in 
    # the corpus (1-dumping_factor)
    len_corpus = len(corpus)
    for p in corpus:
        prob_dist[p] = (1-damping_factor)/len_corpus
    
    # Probability of choosing a link at random linked to by 'page' (dumping_factor)
    len_set = len(corpus[page])
    # Ignore links in the page that link to itself
    if page in corpus[page]:
        len_set -= 1
    for p in corpus[page]:
        prob_dist[p] += damping_factor/len_set
    
    return prob_dist


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create empty dictionaries to store the sampling counts and the 
    # PageRank values
    pageranks = {}
    samplings = {}
    for p in corpus:
        pageranks[p] = 0
        samplings[p] = 0
    
    # Generate first sample randomly
    page = random.choices(list(corpus))[0]
    samplings[page] += 1
    for i in range(0, n-1):
        
        # Get the probability distribuition for each sample starting with the "page"
        # chosen equaly randomly
        prob_dist = transition_model(corpus, page, damping_factor)
    
        # Generate new samples based on the probabilty distribuition of the
        # previous sample
        page = random.choices(list(prob_dist.keys()), 
                              list(prob_dist.values()), 
                              k=1)[0]

        samplings[page] += 1

    # Determine the PageRank for each page (the proportion of all the samples that
    # correspond to that page)
    for p in samplings:
        pageranks[p] += samplings[p]/n    

    return pageranks
        

def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Create empty dictionaries to store the PageRank and NumLinks for each page
    pageranks = {}
    
    # Assign each page a rank of 1/N, where N is the total number of pages in the corpus
    d = damping_factor
    N = len(corpus)
    for p in corpus:
        pageranks[p] = 1/N

    p1 = (1-d)/N

    # Calculate new rank values based on all of the current rank values
    while True:
        current_pageranks = copy.deepcopy(pageranks)
        
        counter = 0
        for i in pageranks:
            sigma = 0
            for j in corpus:
                if len(corpus[j]) == 0:
                    sigma += current_pageranks[j]/N
                    continue
                if i in corpus[j]:
                    sigma += current_pageranks[j]/len(corpus[j])
            
            # PageRank formula
            pageranks[i] = p1 + d*sigma
            
            if abs(pageranks[i] - current_pageranks[i]) > 0.001:
                counter += 1
        
        # Break the loop if the PageRank values don't change
        if counter == 0:
            break
            
    return pageranks
        

if __name__ == "__main__":
    main()
