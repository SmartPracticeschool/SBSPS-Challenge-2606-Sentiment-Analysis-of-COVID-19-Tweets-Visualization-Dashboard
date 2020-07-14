var jsn={"a":{
"active":[1,2,3,5,1,3,5],"case_date":[2,8,1,6,3,8,2],
"confirmed":[1,0,3,6,2,6,4],"death":[5,1,9,3,5,6,7]
},
"b":{
    "abc":[3,9,3,6,9,2],"bbb":[9,1,5,2,7,3]
}
}
var data=new Array();
var data1=Object.values(jsn['a'])
var data2=Object.values(jsn['b'])

var full=""
for(var i=0; i<data1[0].length;i++) 
{
    var row = [data1[0][i],data1[1][i],data1[2][i],data1[3][i]]
    x=row.join();
    full=full.concat("\n")
    full=full.concat(x) 
}
console.log(full)


