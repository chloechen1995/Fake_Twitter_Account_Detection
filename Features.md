
# Features Used to Detect Fake Accounts
## Profile-based Information
<li>Number of followers</li>
<li>Number of tweets</li>
<li>Fo-fo ratio: the ratio of the number of an account's following to its followers</li>
<li>Reputaion score</li>
<li>Following choice: $F=\frac{T_n}{D_n}$    
where $T_n$ is the total number of names among the account's followings and $D_n$ is the number of distinct first names. This ratio attempts to detect whether an account likely used a list of names to pick its folloings or not.[4]</li>

## Content-based Feature
<li>The percentage of Tweets containing URLs</li>
<li>The ratio of the number of unique URLs [3]</li>
<li>hashtag ratio</li>
<li>The ratio of the number of @usernames [3]</li>
<li>The ratio of the number of unique @usernames [3]</li>
<li>Tweet similarity:   
(1) $S=\frac{\sum_{p\in P}c(p)}{l_al_p}$    
where $P$ is the set of possible tweet-to-tweet combinations among any two tweets logged for a certain account, $p$ is a single pair, $c(p)$ is a function calculation the number of words two tweets shere, $l_a$ is the average length of tweets posted by that user, and $l_p$ is the number of tweet combinations. A profile sending similar tweets will have a low value of S.[4]    
(2) $\sum_{a,b \in set of pairs in tweets}\frac{similarity(a,b)}{|set of pairs in tweets|}$    
where the content similarity is computed using the standard cosine simility over the bag-of-word vector representation $\mathbf{V(a)}$ of the tweet contet: $similarity(a,b)=\frac{\mathbf{V(a)}\mathbf{V(b)}}{|\mathbf{V(a)}||\mathbf{V(b)}|}$ 
Since tweets are extremely short (140 characters or less), we consider a bag-of-words model and a sparse bigrams model. [3]</li>
<li>Duplicate tweet count</li>  
<li>User behavior: number of times the user was mentioned, number of times the user was replied to, number of times the user replied someone

## Graph-based Feature
If we view each Twitter account $i$ as a node and each follow relationship as a directed edge $e$, then we can view the whole Twittersphere as a directed graph $G = (V, E)$. Even though the spammers can change their tweeting or following behavior, it will be difficult for them to change their positions in this graph.

### Basic Methods [5]
<li>$indegree\ d_I(v_i)$ of a node $v_i$: the number of nodes that are adjacent to node $v_i$ stands for the  number of followers</li>
<li>$outdegree\ d_O(v_i)$ of a node $v_i$: the number of nodes that are adjacent to $v_i$ stands for the number of friends</li>
<li>reputation: $R(v_i)=\frac{d_I(v_i)}{d_I(v_i)+d_O(v_i)}$</li>    

### More Complicated [1]
<li><strong>Local Clustering Coefficient:</strong> The local clustering coefficient for a vertex is the proportion of links between the vertices within its neighborhood divided by the number of links that could possibly exist between them. This metric can be utilized to quantify how close a vertex’s neighbors are to being a clique.    
$$LG(v)=\frac{2|e^v|}{K_v(K_v-1)}$$
where $K_v$ is the sum of the indegree and outdegree of vertex $v$, and $|e^v|$ is the total number of edges built by all $v$'s neighbors.    
Since legitimate users usually follow accounts whose owners are their friends, colleagues or family members, these accounts are likely to have a relationship with each other. However, since spammers usually blindly follow other accounts, these accounts usually do not know each other and have a looser relationship among them. Thus, compared with the legitimate accounts, Twitter spammers will have smaller local clustering coefficient.</li>
<li><strong>Betweenness Centrality:</strong> Betweenness centrality [4] is a centrality measure of a vertex within a graph. Vertices that occur on many shortest paths between other vertices have a higher betweenness than those that do not. This metric reflects the position of the vertex in the graph. Nodes that occur in many shortest paths have higher values of betweenness centrality. A Twitter spammer will typically use a shotgun approach to finding victims, which means it will follow many accounts without regard for whom they are or with whom these victims are connected. As a result, many of their victims are unrelated accounts, and thus their shortest path between each other is the average shortest path between all nodes in the graph. When the Twitter spammer follows these unrelated accounts, this creates a new shortest path between any victim following of the spam account and any other victim following, through the spam account. Thus, the betweenness centrality of the spammer will be high.</li>
<li><strong>Bi-directional Links Ratio:</strong> If two accounts follow with each other, we con- sider them to have a bidirectional link between each other. The number of bi- directional links of an account reflects the reciprocity between an account and its followings. Since Twitter spammers usually follow a large number of legitimate accounts and cannot force those legitimate accounts to follow back, the number of bi-directional links that a spammer has is low. On the other hand, a legiti- mate user is likely to follow his friends, family members, or co-workers who will follow this user back. Thus, this indication can be used to distinguish spammers. However, Twitter spammers could evade this by following back their followers.
$$R_{bilink}=\frac{N_{bilink}}{N_{fing}}$$
where $N_{bilink}$ and $N_{fing}$ denote the number of bi-directional links and the num- ber of followings. The intuition behind this feature is that even though the spam- mers can increase the value of Nbilink through following back their followers or obtaining “following-backs” from other accounts, compared with their high val- ues of $N_{fing}$, their values of $R_{bilink}$ will be relatively difficult to increase to be comparable with that of legitimate accounts. Although this feature still can be evaded, the spammers need to pay more to evade this feature.</li>

## Neighbor-based Features [1]
<li><strong>Average Neighbors’ Followers:</strong> Average neighbors’ followers of an account represents the average number of followers of this account’s followings. This feature reflects the quality of the choice of friends of an account. It is obvious that legitimate accounts intend to follow the accounts who have higher quality unlike the spammers. Thus, the average neighbors’ followers of legitimate accounts are commonly higher than that of spammers.</li>
<li><strong>Average Neighbors’ Tweets:</strong> Similar to the average neighbors’ followers, since an account’s tweet number could also reflect this account’s quality, we design another feature, named average neighbors’ tweets, which is the average number of tweets of this account’s following accounts. Note that these two features can be evaded by following popular Twitter accounts. We also design another relatively robust neighbor-based detection feature, named followings to median neighbors’ followers.</li>
<li><strong>Followings to median neighbors’ followers:</strong>
$$R_{fing_mnfer}=\frac{N_{fing}}{M_{nfer}}$$
where $M_nfer$ is the median number of an account's all following accounts’ follower numbers </li>

## Automation-based Features [1]
Due to the large cost of manually managing a large number of spam accounts, many spammers choose to create a custom program using Twitter API to post spam tweets.
<li><strong>API Ratio:</strong> API ratio is the ratio of the number of tweets with the tweet source of “API” to the total number of tweet count. As existing work shows, many bots choose to use API to post tweets, so a high API ratio implies this account is more suspicious.</li>
<li><strong>API URL Ratio:</strong> API URL ratio is the ratio of the number of tweets contain- ing a URL posted by API to the total number of tweets posted by API. Since it is more convenient for spammers to post spam tweets using API, especially when spammers need to manage a large amount of accounts. Thus, a higher API URL ratio of an account implies that this account’s tweets sent from API are more likely to contain URLs, making this account more suspicious.</li>
<li><strong>API Tweet Similarity:</strong> Spammers can use tricks to evade the detection feature of tweet similarity and still choose to use API to automatically post malicious tweets. Thus, we also design API tweet similarity, which only compute the similarity of those tweets posted by API. Thus, a higher API tweet similarity of an account implies that this account is more suspicious.</li>

## Timing-based Features
<li><strong>Tweeting rate:</strong> the minimum, maximum, average, and median of the time between tweets, number of tweets posted per day and per week [2]</li>
<li><strong>Following Rate:</strong> Following rate reflects the speed at which an account follows other accounts. Since spammers will usually follow many other accounts in a short period of time, a high following rate of an account indicates that the account is likely a spam account. Since it is difficult to collect the time when an account follows another account, we use the ratio of an account’s following number to the age of the account at the time to obtain an approximate value. [1]</li>

Reference:    
[1] C. Yang, R. Harkreader, and G. Gu. Empirical evaluation and new design for fighting evolving Twitter spammers. I.    
[2] F. Benevenuto, G. Magno, T. Rodrigues, and V. Almeida. Detecting Spammers on Twitter. In Collaboration, Electronic messaging, Anti-Abuse and Spam Confference.    
[3] K. Lee, J. Caverlee, and S. Webb. Uncovering Social Spammers: Social Honeypots Machine Learning. In ACM SIGIR Conference (SIGIR), 2010.    
[4] G. Stringhini, S. Barbara, C. Kruegel, and G. Vigna. Detecting Spammers On Social Networks. In Annual Computer Security Applications Conference (ACSAC’10), 2010.    
[5] A. Wang. Don’t follow me: spam detecting in Twitter. In Int’l Conferene on Security and Cryptography (SECRYPT), 2010.    
