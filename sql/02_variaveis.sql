-- Cadastro das variáveis medidas (dim_variavel).
-- Idempotente: pode ser executado várias vezes; se a variável já existe, atualiza nome, unidade e agregação.

SET client_encoding = 'UTF8';

INSERT INTO dim_variavel (codigo, nome, unidade, agregacao) VALUES
    ('precipitacao',   'Precipitação total horária',     'mm', 'soma'),
    ('temperatura_ar', 'Temperatura do ar (bulbo seco)', '°C', 'media')
ON CONFLICT (codigo) DO UPDATE SET
    nome      = EXCLUDED.nome,
    unidade   = EXCLUDED.unidade,
    agregacao = EXCLUDED.agregacao;