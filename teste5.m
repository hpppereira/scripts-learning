

%h=dire(4,:)';

h1=find(h>0);
h2=diff(h1);
h2=[0;h2];
g=find(h2==4);
if length(g)>0,
for i=1:length(g),
    x=sum(h(h1(g(i)-1))+h(h1(g(i))))/2;  
    h(h1(g(i)-1)+2)=x;
end
end;

h1=find(h>0);
h2=diff(h1);
h2=[0;h2];
g=find(h2==3);
if length(g)>0,
for i=1:length(g),
    x=sum(h(h1(g(i)-1))+h(h1(g(i))))/2;  
    x1=sum(h(h1(g(i)-1))+x)/2; 
    h(h1(g(i)-1)+1)=x1;
    x2=sum(h(h1(g(i)))+x)/2; 
    h(h1(g(i)-1)+2)=x2;
end
end;

h1=find(h>0);
h2=diff(h1);
h2=[0;h2];
g=find(h2==2);
if length(g)>0,
for i=1:length(g),
    x=sum(h(h1(g(i)-1))+h(h1(g(i))))/2;  
    h(h1(g(i)-1)+1)=x;
end
end;
h1=find(h>0);
h2=diff(h1);
h2=[0;h2];


% for i=1:248,
%     if h(i)==0,s1=[s1;i];end
% 
% 
% h=dire(4,:);
% 
% for i=2:247,
%     if h(i)==0,
%         if h(i+1)>0,if h(i-1)>0, h(i)=sum(h(i-1)+h(i+1))/2;end;end
%     end;
% end;
% for i=2:247,
%     if h(i)==0,
%         if h(i+1)>0,if h(i-1)>0, h(i)=sum(h(i-1)+h(i+1))/2;end;end
%     end;
% end;


