%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%PROGRAM spikes.m to eliminate spikes and interpolate
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%Prepared by C. Parente em february 2003
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% the 3 series are investigated
for i=1:3,
   q=a(:,i+1);
   q=[q(1);q;q(end)];
   %a given threshold can be established; here is 500 cm
   
   if abs(q(1))>500,q(1)=0;end
   if abs(q(end))>500,q(end)=0;end;
   g=find(abs(q)>500);g7=g;
   g1=isempty(g);
   if g1==0,
      g=[g;2000];
      while length(g)>1,n=1;
          x1=g(1)-1;
          x=diff(g);
          while x(1)==1,n=n+1;
              x=x(2:end);
          end;
          x2=g(n)+1;
          w1=[x1;x2];w2=[q(x1);q(x2)];
          w=(x1+1:x2-1)';
          %linear interpolation
          
          w3=interp1(w1,w2,w);
          q(w)=w3;
          g=g(n+1:end);
      end;
      a(:,i+1)=q(2:end-1);
   end;
end;



   

            