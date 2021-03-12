# FIFA Online 4 - Players2Vec
피파온라인4(nexon)게임상의 선수 카드의 스탯과, 카드에 대한 유저들의 평가(댓글) 분석을 통한 카드(선수) 추천 시스템

### FIFA online 4 comment/stat data
>- crawled player comment/stat data(http://fifaonline4.inven.co.kr/)
>- repository(includes crawling codes, [Repository](https://github.com/Yeeun-Lee/fifaonline4_aaaab))

### Embed players with ngram
댓글에서 같이 언급한 횟수가 많을 수록 연관 관계가 높다고 추측해볼 수 있음.
> 게임상에서 선수 카드로 더 좋은 팀을 조합하는 등으로 사용되고 있기 때문에, 합이 좋은 선수나, 대체할만한 선수를 언급하고 있을것이라는 가정

[players2vec/w2v_player]
- pandas, numpy, random
- tensorflow.keras

### Cosine-Similarity with player stat data
선수 카드의 stat, 즉 속력, 가속력, 슛 파워 등, 카드가 가지고 있는 고유 능력치 비교를 통해 비슷한 스탯의 선수를 반환함.

### Presentation(Slack API - bot)
slack api에서 제공하는 bot기능을 통해 채팅으로 비교하고자 하는 선수를 입력하거나, 해당 선수와 비슷한 선수를 반환할 수 있도록 연결함

[app.py]
- slacker.Slacker
- slackClient.SlackClient
- Flask

