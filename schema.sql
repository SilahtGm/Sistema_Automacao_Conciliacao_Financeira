-- TABELA DE NOTAS FISCAIS
CREATE TABLE IF NOT EXISTS nota_fiscal (
    id_nf           INTEGER PRIMARY KEY,
    chave_acesso    TEXT NOT NULL,
    fornecedor      TEXT NOT NULL,
    cnpj_fornecedor TEXT NOT NULL,
    descricao       TEXT NOT NULL,
    nf_valor        REAL NOT NULL,
    data_emissao    DATE NOT NULL,
    data_vencimento DATE NOT NULL,
    categoria       TEXT NOT NULL
);

-- TABELA DE LANÇAMENTOS CONTÁBEIS
CREATE TABLE IF NOT EXISTS lancamento_contabil (
    id_lc           INTEGER PRIMARY KEY,
    id_nf           INTEGER NOT NULL,
    fornecedor      TEXT NOT NULL,
    cnpj_fornecedor TEXT NOT NULL,
    descricao       TEXT NOT NULL,
    lc_valor        REAL NOT NULL,
    data_lancamento DATE NOT NULL,
    conta_debito    TEXT NOT NULL,
    conta_credito   TEXT NOT NULL,
    FOREIGN KEY (id_nf) REFERENCES nota_fiscal(id_nf)
);

-- TABELA DE CONCILIAÇÃO
CREATE TABLE IF NOT EXISTS conciliacao (
    id_conciliacao      INTEGER PRIMARY KEY AUTOINCREMENT,
    id_lc               INTEGER NOT NULL,
    id_nf               INTEGER NOT NULL,
    descricao           TEXT NOT NULL,
    valor_nota_fiscal   REAL NOT NULL,
    valor_lancamento    REAL NOT NULL,
    status              TEXT NOT NULL,
    data_conciliacao    DATE NOT NULL,
    FOREIGN KEY (id_lc) REFERENCES lancamento_contabil(id_lc),
    FOREIGN KEY (id_nf) REFERENCES nota_fiscal(id_nf)
);

-- TRIGGER DE CONCILIAÇÃO AUTOMÁTICA
CREATE TRIGGER IF NOT EXISTS trigger_conciliacao_pos_lancamento
AFTER INSERT ON lancamento_contabil
FOR EACH ROW
BEGIN

    INSERT INTO conciliacao (
        id_lc,
        id_nf,
        descricao,
        valor_nota_fiscal,
        valor_lancamento,
        status,
        data_conciliacao
    )
    SELECT
        NEW.id_lc,
        NEW.id_nf,
        CASE
            WHEN NEW.lc_valor < nf.nf_valor THEN 'VALOR LANCADO MENOR QUE A NOTA'
            WHEN NEW.lc_valor > nf.nf_valor THEN 'VALOR LANCADO MAIOR QUE A NOTA'
            ELSE 'VALOR CORRETO'
        END,
        nf.nf_valor,
        NEW.lc_valor,
        CASE
            WHEN NEW.lc_valor = nf.nf_valor THEN 'EM CONFORMIDADE'
            ELSE 'DIVERGENCIA'
        END,
        datetime('now')
    FROM nota_fiscal nf
    WHERE nf.id_nf = NEW.id_nf;
END;

-- VALIDA SE EXISTE ALGUMA NOTA FISCAL PARA ELE LANÇAMENTO
CREATE TRIGGER IF NOT EXISTS trigger_validar_antes_de_lancar
BEFORE INSERT ON lancamento_contabil
FOR EACH ROW
BEGIN
    -- CANCELA O INSERT SE A NOTA FISCAL NÃO EXISTIR OU NÃO POSSUIR VALOR
    SELECT RAISE(ABORT, 'Erro: Nota Fiscal nao encontrada ou sem valor definido.')
    WHERE (SELECT nf_valor FROM nota_fiscal WHERE id_nf = NEW.id_nf) IS NULL;
END;

-- VALIDA SE APÓS A INSERÇÃO DE UMA NOTA FISCAL, EXISTE UM LANÇAMENTO
-- CASO NÃO EXISTA, NÃO INSERE NADA EM CONCILIACAO
CREATE TRIGGER IF NOT EXISTS trigger_conciliacao_pos_nota
AFTER INSERT ON nota_fiscal
FOR EACH ROW
BEGIN
    INSERT INTO conciliacao (id_lc, id_nf, descricao, valor_nota_fiscal, valor_lancamento, status, data_conciliacao)
    SELECT
        l.id_lc,
        NEW.id_nf,
        CASE
            WHEN l.lc_valor < NEW.nf_valor THEN 'VALOR LANCADO MENOR QUE A NOTA'
            WHEN l.lc_valor > NEW.nf_valor THEN 'VALOR LANCADO MAIOR QUE A NOTA'
            ELSE 'VALOR CORRETO'
        END,
        NEW.nf_valor,
        l.lc_valor,
        CASE
            WHEN l.lc_valor = NEW.nf_valor THEN 'EM CONFORMIDADE'
            ELSE 'DIVERGENCIA'
        END,
        datetime('now')
    FROM lancamento_contabil l
    WHERE l.id_nf = NEW.id_nf;
END;