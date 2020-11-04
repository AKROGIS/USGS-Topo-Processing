
-- List best available 1:250k (qm) topo maps
SELECT * FROM [Scratch].[dbo].[qmtopos] where best_topo = 1 order by dups

--check that dates are well ordered  
select cell_name, series, shaded_relief, date, rev, printed from qmtopos
where 1899 > date or date > coalesce(rev, date) or coalesce(rev, date) > printed or printed > 1996

-- get count of maps per unique cell names
select cell_name, count(*) from qmtopos group by Cell_name

-- get count of unique cell names (all series)
select count(*) from (select 1 from qmtopos group by Cell_name) as t (c)

-- get count of unique cell names (for topo series)
-- This returns 152 out of the expected 153, because the Eagle E cell is only for really old topos
select count(*) from (select 1 from qmtopos where series = 'topographic' group by Cell_name) as t (c)
select count(*) from qmtopos where Best_topo = 1

-- get count of unique cell names (for shaded_relief series)
select count(*) from (select 1 from qmtopos where Shaded_Relief = 1 group by Cell_name) as t (c)
select count(*) from qmtopos where Best_sr = 1

-- get count of unique cell names (for bathymetric series)
select count(*) from (select 1 from qmtopos where series = 'bathymetric' group by Cell_name) as t (c)
select count(*) from qmtopos where Best_bath = 1

-- get count of unique cell names (for military series)
select count(*) from (select 1 from qmtopos where left(series,4) = 'Q501' group by Cell_name) as t (c)
select count(*) from qmtopos where Best_mil = 1

-- get dups in best of groups
select Cell_name, count(*) from qmtopos where Best_topo = 1 group by Cell_name having count(*) > 1
select Cell_name, count(*) from qmtopos where best_bath = 1 group by Cell_name having count(*) > 1
select Cell_name, count(*) from qmtopos where best_sr = 1 group by Cell_name having count(*) > 1
select Cell_name, count(*) from qmtopos where Best_mil = 1 group by Cell_name having count(*) > 1

-- get cells in a series with no best of
-- All cells should have a best_topo, except Eagle E
select t1.Cell_name, t2.cell_name from 
(select Cell_name from qmtopos group by Cell_name) as t1
full outer join
(select Cell_name from qmtopos where best_topo = 1 group by Cell_name) as t2
on t1.cell_name = t2.cell_name where t1.cell_name is null or t2.cell_name is null

select t1.Cell_name, t2.cell_name from 
(select Cell_name from qmtopos where series = 'topographic' group by Cell_name) as t1
full outer join
(select Cell_name from qmtopos where best_topo = 1 group by Cell_name) as t2
on t1.cell_name = t2.cell_name where t1.cell_name is null or t2.cell_name is null

select t1.Cell_name, t2.cell_name from 
(select Cell_name from qmtopos where series = 'bathymetric' group by Cell_name) as t1
full outer join
(select Cell_name from qmtopos where best_bath = 1 group by Cell_name) as t2
on t1.cell_name = t2.cell_name where t1.cell_name <> t2.cell_name

select t1.Cell_name, t2.cell_name from 
(select Cell_name from qmtopos where Shaded_Relief = 1 group by Cell_name) as t1
full outer join
(select Cell_name from qmtopos where best_sr = 1 group by Cell_name) as t2
on t1.cell_name = t2.cell_name where t1.cell_name <> t2.cell_name

select t1.Cell_name, t2.cell_name from 
(select Cell_name from qmtopos where left(series,4) = 'Q501' group by Cell_name) as t1
full outer join
(select Cell_name from qmtopos where best_mil = 1 group by Cell_name) as t2
on t1.cell_name = t2.cell_name where t1.cell_name <> t2.cell_name


-- List dups (grouped)
select cell_name, series, shaded_relief, date, rev, printed, Notes, count(*) from 
qmtopos group by cell_name, series, shaded_relief, date, rev, printed, Notes
having count(*) > 1

-- find all maps that have a dup (join with previous query)
select sn, dups, cnt from qmtopos as q1 join
(select cell_name, series, shaded_relief, date, coalesce(rev,1) as rev, printed, Notes, count(*) as cnt from 
qmtopos group by cell_name, series, shaded_relief, date, rev, printed, Notes
having count(*) > 1 ) as q2
on q1.Cell_name = q2.Cell_name and q1.series = q2.series and q1.shaded_relief = q2.shaded_relief 
and q1.date = q2.date and coalesce(q1.rev,1)  = q2.rev and q1.printed = q2.printed and coalesce(q1.Notes,'') = coalesce(q2.Notes,'')

-- Find those that probably have an assumed print date
select * from qmtopos where recon = 1 and date = printed and rev is null and date < 1955

-- Add columns for tracking dups and no print date
alter table qmtopos add dups smallint
alter table qmtopos add nopd smallint

 -- Update dup count
update q1 set dups = cnt from qmtopos as q1 join
(select cell_name, series, shaded_relief, date, coalesce(rev,1) as rev, printed, Notes, count(*) as cnt from 
qmtopos group by cell_name, series, shaded_relief, date, rev, printed
having count(*) > 1 ) as q2
on q1.Cell_name = q2.Cell_name and q1.series = q2.series and q1.shaded_relief = q2.shaded_relief 
and q1.date = q2.date and coalesce(q1.rev,1)  = q2.rev and q1.printed = q2.printed and coalesce(q1.Notes,'') = coalesce(q2.Notes,'')

-- Update a "No print date" flag
update qmtopos set nopd = 1 where recon = 1 and date = printed and rev is null and date < 1955

