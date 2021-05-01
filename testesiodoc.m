



zco=heave;
zdd=pitch_corr;
zdc=roll_corr;

angulo=zeros(744,1);coere1=zeros(744,64);coere2=coere1;tp=zeros(744,1);
for kkl=1:744, n1=0;n2=0;
    qq1=spectrum(zco(:,kkl),zdd(:,kkl),128,64);
    qq9=smooth(qq1(2:65,1),1);
    g2=find(qq9(:,1)==max(qq9(:,1)));tp(kkl)=g2;
%     if g2<8,arq=[0 0 1];end
%     if g2>24,arq=[1 0 0];end;
%     if g2<25,if g2>15,arq=[1 0 1];end;end
%     if g2<16,if g2>7,arq=[0 0 0];end;end
    qq3=qq1(2:65,1);g1=find(qq3(12:16)==max(qq3(12:16)));g1=g1+11;
    qq7=qq1(2:65,3);coere1(kkl,:)=qq1(2:65,5)';
    qq2=spectrum(zco(:,kkl),zdc(:,kkl),128,64);
    qq8=qq2(2:65,3);coere2(kkl,:)=qq2(2:65,5)';
    
%     if qq1(g1,5)>0.8,n1=1;end;
%     if qq2(g1,5)>0.8,n2=1;end;
%     if (n1+n2)>=1,
  if g1>11,
    bc1=-imag(qq1(g1,3));bc2=-imag(qq2(g1,3));
    bc3=angle(bc1+j*bc2);bc3=270-bc3*180/pi-22;
    g=find(bc3<0);bc3(g)=bc3(g)+360;
    g=find(bc3>360);bc3(g)=bc3(g)-360;
    angulo(kkl)=bc3;
    end;
end;
 