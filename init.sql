CREATE TABLE IF NOT EXISTS empresas (
    id_pk INT AUTO_INCREMENT PRIMARY KEY,
    cnpj_empresa VARCHAR(50) NOT NULL UNIQUE,
    codigo_integracao VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS clientes (
    id_pk INT AUTO_INCREMENT PRIMARY KEY,
    cnpj_empresa VARCHAR(50) NOT NULL,
    phone_number VARCHAR(20) NOT NULL,
    cliente VARCHAR(100) NOT NULL,
    CONSTRAINT unique_cnpj_phone UNIQUE (cnpj_empresa, phone_number),
    CONSTRAINT fk_empresa FOREIGN KEY (cnpj_empresa) REFERENCES empresas(cnpj_empresa) ON DELETE CASCADE
);
