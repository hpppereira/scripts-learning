
[b a]=butter(3,0.3);
ventodir=zeros(1,248);

www50=load('ERA_1106.txt');www50=www50';
for ik=1:1,
    h=www50(2,:)';hhh=www50(1,:)';
    teste5
    hh=h*2*pi/360;
    s1=[];s2=[];g3=[];ss1=[];
    hh=[hh;0];hhh=[hhh;0];
    
%     for i=1:length(h2),
%         ss1=h(
        
    for i=1:249 ,
        
        
        if hh(i)>0,
            s1=[s1;hh(i)];ss1=[ss1;hhh(i)];
            s2=[s2;i];
                 
        else;   
           
            if length(s1)>9,
                z1=ss1.*cos(s1);z1=filtfilt(b,a,z1);
                z2=ss1.*sin(s1);z2=filtfilt(b,a,z2);
                g3=angle(z1+j*z2);g3=g3*360/(2*pi);
                             
                g4=find(g3<0);g3(g4)=g3(g4)+360;
                g4=find(g3>=360);g3(g4)=g3(g4)-360;
                                
                ventodir(ik,s2(1):s2(end))=g3;
                s1=[];s2=[];g3=[];ss1=[];
            else;
                if length(s1)>0,
                ventodir(ik,s2(1):s2(end))=s1*180/pi;
                s1=[];s2=[];g3=[];ss1=[];
                end;
            end;
        end;
    end;
end
   

              
%               
%               
%               
%               g=find(hh>0);
%     g1=diff(g);
%     g2=find(g1>1);
%     k=zeros(2,length(g2)-1);
%     for i=1:length(g2),
%         k(1,i)=g(g2(i));
%         k(2,i)=g(g2(i))+g1(g2(i));
%     end;
%     g8=diff(k);
%     
%     
%     
%     x=espe(ik,:);
%     y=hh;
%     ddir1(ik,:)=hh;
%     y=y*2*pi/360;
%     g=find(y==0);
%     for i=1:length(g)-2,
%         z=y(g(i+1):g(i+2)-1);
%         if length(z)>9,
% 
%             z1=cos(z);z1=filtfilt(b,a,z1);
%             z2=sin(z);z2=filtfilt(b,a,z2);
%             g3=angle(z1+j*z2);g3=g3*360/(2*pi);
%             if g3<0,g3=g3+360;end;
%             if g3>=360,g3=g3-360;end;
%             ddir1(ik,g(i)+1:g(i+2)-1)=g3;
%         else; ddir1(ik,g(i)+1:g(i+2)-1)=hh(g(i)+1:g(i+2)-1);
%         end;
%     end;
%     g4=find(abs(hh-ddir1(ik,:))>20);
%     ddir1(ik,g4)=hh(g4);
% 
% end
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% 
% % for ii=1:8:241, %10:241,
% %         g=0;x1=0;x2=0;g4=0;
% % 
% %         g1=ii:ii+7;
% %         s=dire(ik,g1);
% % 
% %         %ss=diff(s');
% %         g6=find(s==0);
% %         if length(g6)<3,
% % 
% %             s1=[];g=[];g4=(ii:ii+7)';
% % 
% %             for i=1:8,
% %                 s2=s(i);
% %                 if s2>0,
% %                     s1=[s1;s2];
% %                     g=[g;g1(i)];
% %                 end;
% %             end;
% %             s3=diff(s1);s3=[1;s3];
% %             g2=find(s3==0);
% %             for i=1:length(g2),
% %                 s1(g2(i))=1.001*s1(g2(i)-1);
% %             end
% %             if length(s1)>2,
% %                 x1=s1;x2=g;
% %                 p=polyfit(x2,x1,2);
% %                 p1=polyval(p,g4);
% %                 h(g4)=p1;
% %             end;
% %         end;
% %     end
% %     %ddir(ik,:)=h;
% % 
% % 
% % 
% 
% 
% 
% 
% %
% %         s=dire(2,:);
% %
% %         g=find(s(1:20)>0);
% %     x1=s(g);x2=g;
% %
% %     s(g)=p1;
% %     sf11
% %     x=espe(ik,:);
% %     y=dire(ik,:);
% %     y=y*2*pi/360;
% %     g=find(x==0);
% %     for i=1:length(g)-1,
% %
% %         if length(z)>9,
% %             z1=cos(z);z1=filtfilt(b,a,z1);
% %             z2=sin(z);z2=filtfilt(b,a,z2);
% %             g3=angle(z1+j*z2);g3=g3*360/(2*pi);
% %             if g3<0,g3=g3+360;end;
% %             if g3>=360,g3=g3-360;end;
% %             ddir1(ik,g(i)+1:g(i+1)-1)=g3;
% %         else; ddir1(ik,g(i)+1:g(i+1)-1)=dire(ik,g(i)+1:g(i+1)-1);
% %         end;
% %     end;
% %     g4=find(abs(dire(ik,:)-ddir1(ik,:))>20);
% %     ddir1(ik,g4)=dire(ik,g4);
% %     
% % end
% % s
% 
% % y=y*2*pi/360;
% %     y=unwrap(y);
% %     y1=cos(y);y2=sin(y);
% %     y1=filtfilt(b,a,y1);
% %     y2=filtfilt(b,a,y2);
% %     
% %     
% %     
% % end;
% % 
% % 
% 
% 
% 

