select
    mm.title,
    ta.score
from
    `pynltk`.t_analyzed ta

join
    `pynltk`.t_review tr
on
    tr.code = ta.code

join
    `pynltk`.m_movie mm
on
    mm.code = tr.movie_code

order by
    mm.code
;
