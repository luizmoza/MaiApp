function search(str, a) { return str.search(a); }
function Len(s){return s.length;}
function Rounder(num, a) { return Math.round(num * Math.pow(10, a)) / Math.pow(10, a) }
function RounderPerc(num, a) {return Math.round(num * 100 * Math.pow(10, a)) / Math.pow(10, a) + '%'}
function Left(str, n){if (n <= 0)return "";else if (n > String(str).length)return str;else return String(str).substring(0,n);}
function trim(str){ var orig = str;if(typeof(orig)=="string"){return orig.trim();}else{return '';}}
function Right(str, n){ if (n <= 0) return ""; else if (n > String(str).length) return str; else {var iLen = String(str).length; return String(str).substring(iLen, iLen - n); }}
function EmpilharObjetos(obj1,obj2){ var obj3 = {}; for (var attrname in obj1) { obj3[attrname] = obj1[attrname]; } for (var attrname in obj2) { obj3[attrname] = obj2[attrname]; } return obj3;}
function formatDate(dt) {var d = new Date(dt.date);var mes = d.getMonth();mes = mes + 1;return [d.getFullYear(), Right('0'+mes,2), Right('0'+d.getDate(),2)].join('-');}
function min_date(all_dates) {var min_dt = all_dates[0],min_dtObj = new Date(all_dates[0]);all_dates.forEach(function(dt, index){if ( new Date( dt ) < min_dtObj){min_dt = dt;min_dtObj = new Date(dt);}});return min_dt;}

function IntOnly(input) {var s = document.getElementById(input).value;var regex = /[^0-9]/gi;s = s.replace(regex, '');document.getElementById(input).value = s;}
function NumberOnly(input) {var s = document.getElementById(input).value;var regex = /[^0-9\,]/gi;s = s.replace(regex, '');document.getElementById(input).value = s;}
function NumberOnlyPerc(input) {var s = document.getElementById(input).value;var regex = /[^0-9\,]/gi;s = s.replace(regex, '');document.getElementById(input).value = s+'%';}

function trata_float(s){
if(typeof s == 'number'){s = s.toString()}    
if(s === undefined || s === null){s = '0'}    
var str = s;
var vvperc = false;
spltperc = str.split('%');
if (spltperc.length > 2 ){return '#N/A';}
if (Right(str,1)=='%'){vvperc = true;}
str = str.replace(/[^\d.,-]/g, '');
str = str.trim();
spltcomma = str.split(',');
spltdot = str.split('.');
if (spltcomma.length == 1 && spltdot.length == 2 ){} // Se só tiver um ponto ... sem virgua
else if (spltcomma.length == 2 && spltdot.length == 1 ){str = str.replace(",", ".");} // Se só tiver uma vírgula ... sem ponto
else if (spltcomma.length == 1 && spltdot.length == 1 ){} // Sem virgula e sem ponto
else if (spltcomma.length > 2 && spltdot.length > 2 ){return '#N/A'} // Multiplas virgulas e multiplos pontos
else if (spltcomma.length == 2 && spltdot.length > 1 ){str = str.replace(",", "").replace(".", ",");} // Multiplos pontos e uma virgula
else if (spltcomma.length > 1 && spltdot.length == 2 ){return str.replace(".", "");} // Multiplas virgulas e umponto
return str    
}

function formatFloat(s) { //Usar para socar no banco o valor pronto para uso
vvperc = false
if (Right(s,1)=='%'){vvperc = true;}
if (vvperc){
    return (parseFloat(trata_float(s))/100).toString();
}else{
    return parseFloat(trata_float(s)).toString();
}
}
function formatPerc(s) {return (parseFloat(trata_float(s))).toString();}

// Exemplo
// Taxa é 5%... float é 0.05 e perc é 5 
// brl é trocar o único ponto (da casa decimal) . por ,
// tratamento tira todos os outros pontos e garante que só tem ponto na casa decimal ,
// No banco ta tudo sendo armazenado como perc tirando o cadastro de renda fixa e fluxos (para facilitar a conta das calculadoras)
// Em tela está tudo taxa
function to_brl(s) {return s.replace(".", ",");}
function float_to_taxa(s) {return (parseFloat(trata_float(s))*100).toString()+'%';}
function float_to_taxa_brl(s) {return to_brl(float_to_taxa(s));}
function perc_to_taxa(s) {return formatPerc(s)+'%';}
function perc_to_taxa_brl(s) {return to_brl(formatPerc(s)+'%');}
function taxa_to_perc(s) {return formatPerc(s);}
function taxa_to_perc_brl(s) {return to_brl(formatPerc(s))+'%';}
function taxa_to_float(s) {return formatFloat(s);}
function taxa_to_float_brl(s) {return to_brl(formatFloat(s));}
function vl_to_float(s) {return (formatFloat(s));}
function vl_to_float_brl(s) {return to_brl(formatFloat(s));}


