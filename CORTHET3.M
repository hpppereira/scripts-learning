function [theta]= theta(a,b,donv)
      
%     REDUZ AS DIRECOES DE ONDA PARA O NORTE VERDADEIRO      
%     PARAMETROS DE ENTRADA (I) E SAIDA (O)
%     A,B ............... ORDENADAS DAS COMPONENTES

for i=1:length(a);      
    
   if a(i)~=0
   
      theta(i)=atan(abs(b(i))/abs(a(i)))*180/pi;      
      
      if (a(i)>0) & (b(i)>=0)
         theta(i) = 90-theta(i);
      end

      if (a(i)>0) & (b(i)<0)
         theta(i) = 90+theta(i);
      end

      if (a(i)<0) & (b(i)<=0)
         theta(i) = 270-theta(i);
      end

      if (a(i)<0) & (b(i)>0)
         theta(i) = 270+theta(i);
      end
         
   else
      
     if b(i)>=0
        theta(i)=0;
     else  
        theta(i)=180;
     end   
    
   end   
   
   theta(i)=theta(i)-donv;
   
   if (theta(i)<0)
      theta(i)=360+theta(i);
   end   
   
end

