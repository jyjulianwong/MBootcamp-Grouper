# MBootcamp Grouper
A group allocation tool made for The Mockingbird's MBootcamp event.

## What is MBootcamp Grouper?
The Mockingbird A Cappella Society annually hosts an MBootcamp event, aimed at inducting and training new members. Members can fall into one of the four basic voice parts -- soprano, alto, tenor or bass. For this event, members are usually split into groups of SATB singers. Trying to find what the ideal combination of groups is for this event can be a lengthy process, especially by hand. Apart from guaranteeing that each group will have at least one member from each voice part, we also want each group to have a reasonable number of both new members and old members, as well as ensure the overall skill and experience levels of the groups are balanced. MBootcamp Grouper helps you find the ideal group combination for MBootcamp. All you need to do is supply the members' names and voice parts, and what constraints an ideal combination should follow, e.g. have at least 2 new members and not have member A and member B be in the same group.

## How is MBootcamp Grouper built?
- MBootcamp Grouper is the RESTful API of the MBootcamp Grouper service, built using **Flask**, the Python web development framework, and deployed on an **Amazon Web Services (AWS) Elastic Beanstalk** instance. The Server component is responsible for receiving grouping requests, searching for group combinations that match the needs of the request sender, and sending responses back to the sender.
- MBootcamp Grouper (Web App) is the front-end web application of the service, built using **ReactJS**, and deployed using **GitHub Pages**.
