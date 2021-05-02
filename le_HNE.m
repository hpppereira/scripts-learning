arquivo='200907241900.HNE';
[tempo, heave, dspN, dspE] = textread(arquivo, '%f %f %f %f',...
    'headerlines', 11);

X(:,1)=tempo;
X(:,2)=heave;
wavetest_1