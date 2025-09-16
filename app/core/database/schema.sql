CREATE TABLE users(
  id bigserial NOT NULL,
  company_id bigserial NOT NULL,
  group_id bigserial NOT NULL,
  timezone_id smallserial NOT NULL,
  username varchar(60) NOT NULL,
  firtsname varchar(60) NOT NULL,
  lastname varchar(60) NOT NULL,
  patronymic varchar(60),
  created_date date NOT NULL,
  user_lock boolean NOT NULL DEFAULT false,
  "password" varchar(255) NOT NULL,
  "comment" varchar(1000),
    CONSTRAINT pk_users PRIMARY KEY(id)
);
CREATE INDEX idx_users_group_id ON users(group_id);
CREATE INDEX idx_users_timezone_id ON users(timezone_id);
CREATE INDEX idx_users_company_id ON users(company_id);
CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_company_id_group_id ON users(company_id, group_id);
CREATE INDEX idx_users_username_user_lock ON users(username, user_lock);
CREATE INDEX idx_users_id_company_id ON users(id, company_id);
CREATE INDEX idx_users_id_group_id ON users(id, group_id);
CREATE INDEX idx_users_id_property_id ON users(id);
COMMENT ON TABLE users IS 'Таблица пользователей';


CREATE TABLE user_groups(
  id bigserial NOT NULL,
  company_id bigserial NOT NULL,
  group_name varchar(255) NOT NULL,
  "comment" varchar(1000),
  CONSTRAINT pk_user_groups PRIMARY KEY(id)
);
CREATE INDEX idx_user_groups_company_id ON user_groups(company_id);
COMMENT ON TABLE user_groups IS 'Таблица групп пользователей';


CREATE TABLE companies(
  id bigserial NOT NULL,
  property_id bigserial NOT NULL,
  "name" varchar(255) NOT NULL,
  created_date date NOT NULL,
  inn varchar(16) NOT NULL,
  kpp varchar(9) NOT NULL,
  ogrn varchar(13),
  bic varchar(9),
  CONSTRAINT pk_companies PRIMARY KEY(id)
);
CREATE INDEX idx_companies_inn ON companies(inn);
CREATE INDEX idx_companies_kpp ON companies(kpp);
CREATE INDEX idx_companies_ogrn ON companies(ogrn);
CREATE INDEX idx_companies_bic ON companies(bic);
CREATE INDEX idx_companies_property_id ON companies(property_id);
COMMENT ON TABLE companies IS 'Таблица с компаниями';


CREATE TABLE timezone_dict(
  id smallserial NOT NULL,
  timezone_name varchar(255),
  timezone timetz,
  CONSTRAINT pk_timezone_dict PRIMARY KEY(id)
);
COMMENT ON TABLE timezone_dict IS 'Таблица с справчоник таймзон';


CREATE TABLE user_properties(
  id bigserial NOT NULL,
  user_id bigserial NOT NULL,
  property_code_id smallserial NOT NULL,
  "value" varchar(255),
  CONSTRAINT pk_user_properties PRIMARY KEY(id)
);
CREATE UNIQUE INDEX idx_user_properties_property_code_id ON user_properties
  (property_code_id)
;
CREATE INDEX idx_user_properties_property_id ON user_properties(user_id);
CREATE INDEX idx_user_properties_property_id_property_code_id ON user_properties
  (user_id, property_code_id)
;
COMMENT ON TABLE user_properties IS 'Таблица свойств пользователей';


CREATE TABLE property_code_dict(
  id smallserial NOT NULL,
  group_code varchar(30) NOT NULL,
  code varchar(30) NOT NULL,
  "name" varchar(100),
  CONSTRAINT pk_property_code_dict PRIMARY KEY(id)
);
CREATE INDEX idx_property_code_dict_code ON property_code_dict(code);
CREATE INDEX idx_property_code_dict_group_code_code ON property_code_dict
  (group_code, code NULLS LAST)
;
COMMENT ON TABLE property_code_dict IS
  'Таблица справочник кодов для свойств пользователя
PROFILE_IMAGE - путь до картинки с профилем пользователя
USER_MOBILE - телефон пользователя
USER_NUMVER - индиыидуальный номер пользователя'
;


CREATE TABLE roles_dict(
  id smallserial NOT NULL,
  code varchar(30) NOT NULL,
  "name" varchar(60) NOT NULL,
  CONSTRAINT pk_roles_dict PRIMARY KEY(id)
);
COMMENT ON TABLE roles_dict IS 'Таблица справочник ролей пользователя';


CREATE TABLE user_roles(
  id integer NOT NULL,
  user_id bigserial NOT NULL,
  role_id smallserial NOT NULL,
  active_from date NOT NULL,
  active_to date,
  CONSTRAINT pk_user_roles PRIMARY KEY(id)
);
CREATE INDEX idx_user_roles_user_id ON user_roles(user_id);
CREATE INDEX idx_user_roles_role_id ON user_roles(role_id);
CREATE INDEX idx_user_roles_user_id_role_id_active_to ON user_roles
  (user_id, role_id, active_to)
;
CREATE INDEX idx_user_roles_active_from ON user_roles(active_from);
CREATE INDEX idx_user_roles_active_to ON user_roles(active_to);
COMMENT ON TABLE user_roles IS 'Таблица ролей пользователей';


CREATE TABLE role_functions(
  id smallserial NOT NULL,
  role_id smallserial NOT NULL,
  function_code_id smallserial NOT NULL,
  CONSTRAINT pk_role_functions PRIMARY KEY(id)
);
CREATE INDEX idx_role_functions_role_id ON role_functions(role_id);
CREATE INDEX idx_role_functions_function_code_id ON role_functions
  (function_code_id)
;
COMMENT ON TABLE role_functions IS 'Таблица с ролевыми функциями';


CREATE TABLE functions_dict(
  id smallserial NOT NULL,
  code varchar(30) NOT NULL,
  "version" smallserial NOT NULL,
  CONSTRAINT pk_functions PRIMARY KEY(id)
);
COMMENT ON TABLE functions_dict IS 'Таблица справочник ролевых функций';


CREATE TABLE settings(
  id smallserial NOT NULL,
  setting_code_id smallserial NOT NULL,
  "value" varchar(255) NOT NULL,
  active_from date NOT NULL,
  active_to date,
  CONSTRAINT pk_settings PRIMARY KEY(id)
);
CREATE INDEX idx_settings_setting_code_id ON settings(setting_code_id);
CREATE INDEX idx_settings_active_from ON settings(active_from);
CREATE INDEX idx_settings_active_to ON settings(active_to);
CREATE INDEX idx_settings_active_from_active_to ON settings
  (active_from, active_to)
;
CREATE INDEX idx_settings_property_code_id_active_from_active_to ON settings
  (setting_code_id, active_from, active_to)
;
CREATE INDEX idx_settings_setting_code_id_active_to ON settings
  (setting_code_id, active_to)
;
COMMENT ON TABLE settings IS 'Таблица общих свойст';


CREATE TABLE settings_dict(
  id smallserial NOT NULL,
  code varchar(30) NOT NULL,
  "name" varchar(255) NOT NULL,
  CONSTRAINT pk_settings_dict PRIMARY KEY(id)
);
CREATE INDEX idx_settings_dict_code ON settings_dict(code);
COMMENT ON TABLE settings_dict IS 'Таблица справочник кодов системы';


CREATE TABLE license(
  id bigserial NOT NULL,
  company_id bigserial NOT NULL,
  lisense_key varchar(1000) NOT NULL,
  active_from date NOT NULL,
  active_to date NOT NULL,
  CONSTRAINT pk_license PRIMARY KEY(id)
);
CREATE INDEX idx_license_company_id ON license(company_id);
CREATE INDEX idx_license_company_id_active_from ON license
  (company_id, active_from)
;
CREATE INDEX idx_license_active_from_active_to ON license
  (active_from, active_to)
;
CREATE INDEX idx_license_company_id_active_from_active_to ON license
  (company_id, active_from, active_to)
;
COMMENT ON TABLE license IS 'Таблица с лицензиями';


CREATE TABLE modules(
  id integer NOT NULL,
  code varchar(30) NOT NULL,
  "name" varchar(60) NOT NULL,
  CONSTRAINT pk_modules PRIMARY KEY(id)
);
CREATE INDEX idx_modules_code ON modules(code);


COMMENT ON TABLE modules IS 'Таблица дополнительных модулей';


CREATE TABLE module_company_links(
  id bigserial NOT NULL,
  module_id integer NOT NULL,
  company_id bigserial NOT NULL,
  "position" int4 NOT NULL,
  active_from date NOT NULL,
  active_to date,
  CONSTRAINT pk_module_company_links PRIMARY KEY(id)
);
CREATE INDEX idx_module_company_links_company_id ON module_company_links
  (company_id)
;
CREATE INDEX idx_module_company_links_module_id ON module_company_links
  (module_id)
;
CREATE INDEX idx_module_company_links_active_from ON module_company_links
  (active_from)
;
CREATE INDEX idx_module_company_links_active_to ON module_company_links
  (active_to)
;
CREATE INDEX idx_module_company_links_company_id_active_from_active_to ON
  module_company_links(company_id, active_from, active_to)
;
COMMENT ON TABLE module_company_links IS 'Таблица связей модулей и компаний';


CREATE TABLE user_sendings(
  id bigserial NOT NULL,
  user_id bigserial NOT NULL,
  status_id integer NOT NULL,
  created_date date NOT NULL,
  message varchar(4000) NOT NULL,
  CONSTRAINT pk_user_sendings PRIMARY KEY(id),
  CONSTRAINT user_sendings_key UNIQUE(user_id)
);
CREATE INDEX idx_user_sendings_user_id ON user_sendings(user_id NULLS LAST);
CREATE INDEX idx_user_sendings_status_id ON user_sendings(status_id NULLS LAST);
CREATE INDEX idx_user_sendings_user_id_status_id_created_date ON user_sendings
  (user_id, status_id, created_date)
;
CREATE INDEX idx_user_sendings_created_date ON user_sendings(created_date);
COMMENT ON TABLE user_sendings IS 'Таблица рассылки сообщений по пользователям';


CREATE TABLE status_dict(
  id integer NOT NULL,
  code varchar(16) NOT NULL,
  "name" varchar(60) NOT NULL,
  CONSTRAINT pk_status_dict PRIMARY KEY(id)
);
CREATE INDEX idx_status_dict_code ON status_dict(code);


CREATE TABLE shablon_dict(
  id integer NOT NULL,
  code varchar(30) NOT NULL,
  "name" varchar(255) NOT NULL,
  "value" text,
  CONSTRAINT pk_shablon_dict PRIMARY KEY(id)
);
CREATE INDEX idx_shablon_dict_code ON shablon_dict(code);
COMMENT ON TABLE shablon_dict IS 'Таблици справочник шаблонов';


CREATE TABLE reports(
  id integer NOT NULL,
  code varchar(30) NOT NULL,
  "name" varchar NOT NULL,
  "version" int4 NOT NULL,
  CONSTRAINT pk_reports PRIMARY KEY(id)
);
CREATE INDEX idx_reports_code ON reports(code);
CREATE INDEX idx_reports_code_version ON reports(code, "version");
COMMENT ON TABLE reports IS 'Таблица справочник отчетов';


CREATE TABLE user_report_links(
  id bigserial NOT NULL,
  user_id bigserial NOT NULL,
  report_id integer NOT NULL,
  created_date date NOT NULL,
  acive_from date NOT NULL,
  active_to date,
  CONSTRAINT pk_user_report_links PRIMARY KEY(id)
);
CREATE INDEX idx_user_report_links_user_id ON user_report_links(user_id);
CREATE INDEX idx_user_report_links_report_id ON user_report_links
  (report_id NULLS LAST)
;
CREATE INDEX idx_user_report_links_created_date ON user_report_links
  (created_date)
;
CREATE INDEX idx_user_report_links_acive_from ON user_report_links(acive_from);
CREATE INDEX idx_user_report_links_active_to ON user_report_links(active_to);
CREATE INDEX idx_user_report_links_acive_from_active_to ON user_report_links
  (acive_from, active_to)
;
CREATE INDEX idx_user_report_links_user_id_active_to ON user_report_links
  (user_id, active_to)
;
CREATE INDEX idx_user_report_links_user_id_acive_from_active_to ON
  user_report_links(user_id, acive_from, active_to)
;
CREATE INDEX idx_user_report_links_id ON user_report_links(id);
COMMENT ON TABLE user_report_links IS 'Таблица связей отчетов и пользователей';


CREATE TABLE company_properties(
  id bigserial NOT NULL,
  company_id bigserial NOT NULL,
  property_code_id smallserial NOT NULL,
  "value" varchar(255),
  CONSTRAINT pk_company_properties PRIMARY KEY(id)
);
CREATE UNIQUE INDEX idx_company_properties_property_code_id ON
  company_properties(property_code_id)
;
CREATE INDEX idx_company_properties_company_id ON company_properties(company_id);
CREATE INDEX idx_company_properties_company_id_property_code_id ON
  company_properties(company_id, property_code_id)
;
COMMENT ON TABLE company_properties IS 'Таблица свойств компаний';


CREATE TABLE departments(
  id bigserial NOT NULL,
  company_id bigserial NOT NULL,
  code bigserial NOT NULL,
  "name" varchar(255) NOT NULL,
  created_date date NOT NULL,
  CONSTRAINT pk_departments PRIMARY KEY(id)
);
CREATE INDEX idx_departments_code ON departments(code);
CREATE INDEX idx_departments_company_id ON departments(company_id);
COMMENT ON TABLE departments IS 'Таблица с подраздлений';


ALTER TABLE users
  ADD CONSTRAINT users_company_id_fkey
    FOREIGN KEY (company_id) REFERENCES companies (id)
;
ALTER TABLE users
  ADD CONSTRAINT users_group_id_fkey
    FOREIGN KEY (group_id) REFERENCES user_groups (id)
;
ALTER TABLE users
  ADD CONSTRAINT users_timezone_id_fkey
    FOREIGN KEY (timezone_id) REFERENCES timezone_dict (id)
;
ALTER TABLE user_roles
  ADD CONSTRAINT user_roles_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES users (id)
;
ALTER TABLE user_report_links
  ADD CONSTRAINT user_report_links_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES users (id)
;
ALTER TABLE user_sendings
  ADD CONSTRAINT user_sendings_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES users (id)
;
ALTER TABLE user_properties
  ADD CONSTRAINT user_properties_user_id_fkey
    FOREIGN KEY (user_id) REFERENCES users (id)
;
ALTER TABLE user_groups
  ADD CONSTRAINT user_groups_company_id_fkey
    FOREIGN KEY (company_id) REFERENCES companies (id)
;
ALTER TABLE license
  ADD CONSTRAINT license_company_id_fkey
    FOREIGN KEY (company_id) REFERENCES companies (id)
;
ALTER TABLE companies
  ADD CONSTRAINT companies_property_id_fkey
    FOREIGN KEY (property_id) REFERENCES property_code_dict (id)
;
ALTER TABLE module_company_links
  ADD CONSTRAINT module_company_links_company_id_fkey
    FOREIGN KEY (company_id) REFERENCES companies (id)
;
ALTER TABLE company_properties
  ADD CONSTRAINT company_properties_company_id_fkey
    FOREIGN KEY (company_id) REFERENCES companies (id)
;
ALTER TABLE departments
  ADD CONSTRAINT departments_company_id_fkey
    FOREIGN KEY (company_id) REFERENCES companies (id)
;
ALTER TABLE user_properties
  ADD CONSTRAINT user_properties_property_code_id_fkey
    FOREIGN KEY (property_code_id) REFERENCES property_code_dict (id)
;
ALTER TABLE company_properties
  ADD CONSTRAINT company_properties_property_code_id_fkey
    FOREIGN KEY (property_code_id) REFERENCES property_code_dict (id)
;
ALTER TABLE user_roles
  ADD CONSTRAINT user_roles_role_id_fkey
    FOREIGN KEY (role_id) REFERENCES roles_dict (id)
;
ALTER TABLE role_functions
  ADD CONSTRAINT role_functions_role_id_fkey
    FOREIGN KEY (role_id) REFERENCES roles_dict (id)
;
ALTER TABLE role_functions
  ADD CONSTRAINT role_functions_function_code_id_fkey
    FOREIGN KEY (function_code_id) REFERENCES functions_dict (id)
;
ALTER TABLE settings
  ADD CONSTRAINT settings_setting_code_id_fkey
    FOREIGN KEY (setting_code_id) REFERENCES settings_dict (id)
;
ALTER TABLE module_company_links
  ADD CONSTRAINT module_company_links_module_id_fkey
    FOREIGN KEY (module_id) REFERENCES modules (id)
;
ALTER TABLE user_sendings
  ADD CONSTRAINT user_sendings_status_id_fkey
    FOREIGN KEY (status_id) REFERENCES status_dict (id)
;
ALTER TABLE user_report_links
  ADD CONSTRAINT user_report_links_report_id_fkey
    FOREIGN KEY (report_id) REFERENCES reports (id)
;

