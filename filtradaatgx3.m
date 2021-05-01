

ddir=zeros(4,248);
cc=[1;9;17;25;33];ik1=0;
for ik=[4],ik1=ik1+1;
[b a]=butter(4,0.03);
y=dire(:,ik);
y=y*2*pi/360;
y=unwrap(y);
w1=y*360/(2*pi);
y1=cos(y);y2=sin(y);
w=zeros(1,720);
for i=5:712,
    g1=mean(y1(i-4:i+4));
    g2=mean(y2(i-4:i+4));
    g3=angle(g1+j*g2);g3=g3*360/(2*pi);
    if g3<0,g3=g3+360;end;
    if g3>=360,g3=g3-360;end;
    w(i)=g3;
end;


g=find(w>360);
w(g)=w(g)-360;
g=find(w>360);
w(g)=w(g)-360;

g=find(w<0);
w(g)=w(g)+360;

ddir(ik1,1:length(w))=w;
end;
% sf11
% ddir(1,:)=dire(1,:);
% ddir(2,:)=dire(2,:);
% ddir(3,:)=dire(3,:);
% ddir(4,:)=dire(4,:);
% ddir=ddir-23;
% sf11
% for i=1:248,
%     for k=1:2:7,
%         if spr(ceil(k/2),i)>0,
%         espe(k:k+1,i)=espe(k:k+1,i)*spr(ceil(k/2),i)/sum(espe(k:k+1,i));
%     end;end;
% end







