# 3D Student Visualization

Using [t-SNE](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding) to
visualize data collected from the [CyRanch App](https://github.com/sshh12/CyRanch-App-Server).

[Live Code](https://sshh.io/webapps/studentvis/main.html)

## Built Using:

* [db.py](https://github.com/yhat/db.py)
* [scikit-learn](http://scikit-learn.org/stable/)
* [numpy](http://www.numpy.org/)
* [jsSHA](https://github.com/Caligatio/jsSHA)
* [p5js](https://p5js.org/)

## What

With the data collected from the [CyRanch App](https://github.com/sshh12/CyRanch-App-Server), every users
grades were turned into a 7D vector based on their average grade in 7 fields: Science, Math, English, 
(Non-English) Language, Arts, Sports, and Social Studies. Using a dimensionality reduction algorithm, t-SNE, the data
was used to create clusters of students based on their academic performance. While these 3D groupings are
purely abstract, they serve as an interesting way to visualize students and see possible patterns.

### Screenshot

![screenshot](https://cloud.githubusercontent.com/assets/6625384/25551412/3e642c36-2c4a-11e7-84ca-030f6d723ba6.gif)

## Other Visuals

![gpa](https://raw.githubusercontent.com/sshh12/Students-Visualization/master/other_visuals/gpa_stats.png?)

![demo](https://raw.githubusercontent.com/sshh12/Students-Visualization/master/other_visuals/demo_stats.png?)