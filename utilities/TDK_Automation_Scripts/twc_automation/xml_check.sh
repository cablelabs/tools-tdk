##########################################################################
# If not stated otherwise in this file or this component's Licenses.txt
# file the following copyright and licenses apply:
#
# Copyright 2016 RDK Management
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
##########################################################################
#!/bin/bash
#stack_close=("</TestCase>" "</TestFunction>" "</Message>" "</Description>")
stack=(0 0 0 0 )

xml_file=$1
len=${#stack_close[@]}

no_line=$(cat $xml_file |wc -l)
echo "No: of lines::"$no_line
var=0
DCount=1
MCount=1
TFCount=1


#sed '/^$/N;/^\n$/D' sample.txt>sample.txt
while read line
do
  string="$line"
  var=$(( var+1 ))

  if [[ "$line" = *"<Description"* && $DCount = 1 ]]; then 
    #echo "1st description"$var
    stack[3]=1
    if [[ "$line" = *"</Description"* ]];then
        stack[3]=0
    else 
	DCount=$(( DCount+1 ))
    fi

  elif [[ "$line" = *"<Message"* && "$MCount" = 1 ]]; then
    #echo "1st Message"$var
    stack[2]=1
    MCount=$(( MCount+1 ))


  elif [[ "$line" = *"<TestFunction"* && "$TFCount" = 1 ]]; then
    #echo "1st TestFunction"$var
    stack[1]=1
    TFCount=$(( TFCount+1 ))



  elif [[ "$line" = *"<Description"* ]]; then
    if [[ ${stack[3]} = 1 ]]; then
      string="</Description>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
    fi
    if [[ "$line" = *"</Description"* ]]; then 
      stack[3]=0
    else
      stack[3]=1
    fi 


  elif [[ "$line" = *"<Message"* ]]; then
    if [[ ${stack[2]} = 1 ]]; then
      #echo "</Message> inserted<M>" $var 
      string="</Message>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[2]=1
    fi
 	
    if [[ ${stack[3]} = 1 ]]; then
      string="</Description>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[3]=0
    fi
    stack[2]=1


   elif [[ "$line" = *"<TestFunction"* ]]; then
    if [[ ${stack[1]} = 1 ]]; then 
      string="<Incident type=\"Error\"/></TestFunction>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[1]=1
    fi
        
    if [[ ${stack[2]} = 1 ]]; then
      #echo "</Message> inserted<TF>" $var 
      string="</Message>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[2]=0
    fi
 	
    if [[ ${stack[3]} = 1 ]]; then
      string="</Description>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[3]=0
    fi
    stack[1]=1
    #DCount=1
    #MCount=1
    #TFCount=1

 
    


   elif [[ "$line" = "<TestCase"*  ]]; then
    #echo $line
    stack[0]=1



  elif [[ "$line" = *"</TestCase"* ]]; then
    if [[ ${stack[3]} = 1 ]]; then
      string="</Description>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[3]=0
    fi

    if [[ ${stack[2]} = 1 ]]; then
      #echo "</Message> inserted</TC>" $var 
      string="</Message>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[2]=0
    fi
    
    if [[ ${stack[1]} = 1 ]]; then
      string="<Incident type=\"Error\"/></TestFunction>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[1]=0
    fi

    if [[ ${stack[0]} = 1 ]]; then
      stack[0]=0
    fi




  elif [[ "$line" = *"</TestFunction"* ]]; then    
    if [[ ${stack[3]} = 1 ]]; then
      string="</Description>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[3]=0
    fi

    if [[ ${stack[2]} = 1 ]]; then
      #echo "</Message> inserted</TF>" $var 
      string="</Message>${string}"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[2]=0
    fi
    
    if [[ ${stack[1]} = 1 ]]; then
      stack[1]=0
    fi
  	
  

  elif [[ "$line" = *"</Message"* ]]; then
    #echo "$line "$var
    if [[ ${stack[3]} = 1 ]]; then
      #echo "string appended before </Message> " 
      string="</Description>${string}"$var
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[3]=0
    fi
    
    if [[ ${stack[2]} = 1 ]]; then
      stack[2]=0
    fi
    


  elif [[ "$line" = *"</Description"* ]]; then
    if [[ ${stack[3]} = 1 ]]; then
      stack[3]=0
    fi
  
  fi


  

  if [[ $var = $no_line ]];then
    #echo $var
    if [[ ${stack[3]} = 1 ]]; then
      string="${string}</Description>"
      #sed -i "/$line/c\ $string" sample.txt
      #echo $string"::"$var 
      stack[3]=0
    fi

    if [[ ${stack[2]} = 1 ]];then  
      #echo "</Message> inserted EOF" $var 
      string="${string}</Message>"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[2]=0
    fi

    if [[ ${stack[1]} = 1 ]];then  
      string="${string}<Incident type=\"Error\"/></TestFunction>"
      #echo "adding TestFunction end tag"
      #sed -i "/$line/c\ ${string}" sample.txt
      #echo $string"::"$var 
      stack[1]=0
    fi

    if [[ ${stack[0]} = 1 ]];then  
      #echo "<TC insertion>"$var
      string="${string}</TestCase>"
      #echo "adding TestCase end tag: " $string
      #sed -i "/$line/c\ $string" sample.txt
      #echo $string"::"$var 
      stack[0]=0
    fi 
  fi
#echo $var"::"$string

mkdir -p TEMP

if [[ $var = 1 ]];then 
  echo $string>TEMP/output.txt
else 
  echo $string>>TEMP/output.txt
fi
done < $xml_file
mv TEMP/output.txt $xml_file

rm -rf TEMP
