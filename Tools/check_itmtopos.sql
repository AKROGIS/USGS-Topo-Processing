SELECT * FROM itm_data order by [file]

-- Duplicates
select name, [date], Coalesce(revision, [date]) as revision, printed, count(*) as cnt from itm_data group by name, [date], Coalesce(revision, [date]), printed
having count(*) > 1

-- Update Dups field
update q set dups = c.cnt
FROM itm_data as q
left join (select name, [date], Coalesce(revision, [date]) as revision, printed, count(*) as cnt from itm_data group by name, [date], Coalesce(revision, [date]), printed having count(*) > 1) as c
on c.name = q.name and c.[date] = q.[date] and c.revision = Coalesce(q.revision, q.[date]) and c.printed = q.printed

-- Number of tiles in a series/cell
select cell_name, count(*) as cnt from itm_data group by cell_name

-- Update Count field
update q set [count] = c.cnt
FROM itm_data as q
left join (select cell_name, count(*) as cnt from itm_data group by cell_name) as c
on c.cell_name = q.cell_name 

-- All the tiles that have only one file should be best in series by default
select name, best_topo from itm_data where count = 1 order by cell_name

-- Topos with in best of groups
select cell_name, count(*) from itm_data where Best_topo = 1 group by cell_name having count(*) > 1

-- Topos with no best in series selected
select t1.cell_name, t2.cell_name from 
(select cell_name from itm_data group by cell_name) as t1
full outer join
(select cell_name from itm_data where best_topo = 1 group by cell_name) as t2
on t1.cell_name = t2.cell_name where t1.cell_name is null or t2.cell_name is null


-- Create a default best topo (use largest SN for now; This is typical for Afognak)
select cell_name, max(sn) as sn from itm_data where best_topo is null group by cell_name

update q set best_topo = 1
from itm_data as q
left join (select max(sn) as sn from itm_data where best_topo is null group by cell_name) as c
on c.sn = q.sn
where c.sn is not null

update itm_data set best_topo = 0 where best_topo is null