from string import Template

table_template = Template('\
<table> \n\
    <tr> \n\
        <th>Model Class</th> \n\
        <th>Model Type</th> \n\
        <th>Average Word Error Rate</th> \n\
        <th>Average Match Error Rate</th> \n\
        <th>Average Word Information Lost</th> \n\
        <th>Average Word Information Preserved</th> \n\
        <th>Average Character Error Rate</th> \n\
    </tr> \n\
$table_data\
</table> \n\
<p>Last updated: $date</p>\n')
