from automaton import Lexico

l = Lexico()
l.load('config.json')

entrada = """fn main() {
    let a, b, c, media: float; 
    a = 8.2;
    b = 6.5; 
    c = 7.0;
    media = (a + b + c)/3.0;
    
    println("{}", media);
}
"""
l.process(entrada,1)