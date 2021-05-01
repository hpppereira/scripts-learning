function [VDMX,VID]=vetor_dir(VH,VT,Spico,dSpico,fScava,VTZM);
%
% Funcao para calculo das direcoes associadas as alturas individuais
% de onda e direcao associada a onda maxima VZMX 
%
% C.I. Fisch / J.A. LIma 21/07/99
%
% -------------------------------------------------------------------
%
% Lista das alturas, periodos e direcoes individuais
VID=[];
if length(Spico) == 1
   VID=ones(length(VH),1)*dSpico(1);
else
   [auxf k]=sort(fScava);auxd=dSpico(k);
   if length(Spico) == 2
      j=0;
      for n=1:length(VT);
         if VT(n) >= 1/auxf(2)
            j=j+1;VID(j)=auxd(1);
         else
            j=j+1;VID(j)=auxd(2);
         end
      end
   elseif length(Spico) == 3
      j=0;
      for n=1:length(VT);
         if VT(n) >= 1/auxf(2)
            j=j+1;VID(j)=auxd(1);
         elseif VT(n) < 1/auxf(2) & VT(n) >= 1/auxf(3)
            j=j+1;VID(j)=auxd(2);
         elseif VT(n) < 1/auxf(3)
            j=j+1;VID(j)=auxd(3);
         end
      end
   end
   VID=VID';
end
%
% Estimando direcao VDMX da onda maxima
if length(Spico) == 1
   VDMX=dSpico(1);
else
   [auxf k]=sort(fScava);auxd=dSpico(k);
   if length(Spico) == 2
      if VTZM >= 1/auxf(2)
          VDMX=auxd(1);
      else
          VDMX=auxd(2);
      end
   elseif length(Spico) == 3
      if VTZM >= 1/auxf(2)
          VDMX=auxd(1);
      elseif VTZM < 1/auxf(2) & VTZM >= 1/auxf(3)
          VDMX=auxd(2);
      elseif VTZM < 1/auxf(3)
          VDMX=auxd(3);
      end
   end
end

