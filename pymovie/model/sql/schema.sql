use `pynltk`;

drop table if exists `pynltk`.`m_movie`;
create table `pynltk`.`m_movie` (
    `code` int(10) unsigned not null primary key,
    `title` varchar(30),
    `open_date` varchar(50),
    `created` datetime
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


drop table if exists `t_review`;
create table `pynltk`.`t_review` (
    `code` int not null,
    `movie_code` int(10) unsigned not null,
    `points` int not null,
    `content` text not null,
    `empathy` int not null,
    `created` datetime,

    primary key (`code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;