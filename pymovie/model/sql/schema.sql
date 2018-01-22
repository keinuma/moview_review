use `pynltk`;

drop table if exists `pynltk`.`m_movie`;
create table `pynltk`.`m_movie` (
    `code` int(10) unsigned not null primary key,
    `title` varchar(30),
    `open_date` datetime,
    `created` datetime
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


drop table if exists `movie_review`;
create table `pynltk`.`t_review` (
    `code` int not null,
    `movie_code` int(10) unsigned not null,
    `points` int not null,
    `content` text not null,
    `empathy` int not null,
    `created` datetime,

    primary key (`code`),
    foreign key (`movie_code`) references `m_movie`(`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;