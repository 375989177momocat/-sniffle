SELECT  l.g1_id, 
        l.g1_usermininame, 
        l.g1_score,
        @curRow := @curRow + 1 AS row_number
FROM    game1 l 
JOIN    (SELECT @curRow := 0) r
where l.g1_id = 5
order by g1_score DESC limit 100;
#mysql 设置排序后排名
#l 表示原表，r 表示增加表。select后面数据可按照正常写，也可以写*
