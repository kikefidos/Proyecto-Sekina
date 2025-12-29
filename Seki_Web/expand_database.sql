-- Script completo para MVP de plataforma educativa SekiWeb
-- Incluye autenticación con Google, sistema completo de cursos, pagos, notificaciones, etc.
-- Ejecutar después del dump inicial

USE seki_db;

-- =============================================================================
-- ALTERACIONES A TABLAS EXISTENTES
-- =============================================================================

-- 1. Alterar tabla usuarios para MVP completo
ALTER TABLE usuarios
ADD COLUMN telefono VARCHAR(20) NULL AFTER email,
ADD COLUMN fecha_nacimiento DATE NULL AFTER telefono,
ADD COLUMN genero ENUM('M', 'F', 'Otro') NULL AFTER fecha_nacimiento,
ADD COLUMN avatar VARCHAR(255) NULL AFTER genero,
ADD COLUMN biografia TEXT NULL AFTER avatar,
ADD COLUMN activo BOOLEAN DEFAULT TRUE AFTER biografia,
ADD COLUMN ultimo_acceso TIMESTAMP NULL AFTER activo,
ADD COLUMN email_verificado BOOLEAN DEFAULT FALSE AFTER ultimo_acceso,
ADD COLUMN telefono_verificado BOOLEAN DEFAULT FALSE AFTER email_verificado,
ADD COLUMN preferencias_notificaciones JSON NULL AFTER telefono_verificado,
ADD COLUMN idioma_preferido VARCHAR(10) DEFAULT 'es' AFTER preferencias_notificaciones,
ADD COLUMN zona_horaria VARCHAR(50) DEFAULT 'America/Guayaquil' AFTER idioma_preferido;

-- 2. Alterar tabla cursos para MVP
ALTER TABLE cursos
ADD COLUMN precio DECIMAL(10,2) DEFAULT 0.00 AFTER horas,
ADD COLUMN precio_descuento DECIMAL(10,2) NULL AFTER precio,
ADD COLUMN imagen VARCHAR(255) NULL AFTER precio_descuento,
ADD COLUMN video_intro VARCHAR(255) NULL AFTER imagen,
ADD COLUMN categoria_id INT NULL AFTER video_intro,
ADD COLUMN idioma VARCHAR(50) DEFAULT 'Español' AFTER categoria_id,
ADD COLUMN certificado BOOLEAN DEFAULT FALSE AFTER idioma,
ADD COLUMN calificacion_promedio DECIMAL(3,2) DEFAULT 0.00 AFTER certificado,
ADD COLUMN numero_estudiantes INT DEFAULT 0 AFTER calificacion_promedio,
ADD COLUMN numero_calificaciones INT DEFAULT 0 AFTER numero_estudiantes,
ADD COLUMN activo BOOLEAN DEFAULT TRUE AFTER numero_calificaciones,
ADD COLUMN destacado BOOLEAN DEFAULT FALSE AFTER activo,
ADD COLUMN fecha_publicacion TIMESTAMP NULL AFTER destacado,
ADD COLUMN nivel_dificultad ENUM('Principiante', 'Intermedio', 'Avanzado') DEFAULT 'Intermedio' AFTER fecha_publicacion,
ADD COLUMN requisitos TEXT NULL AFTER nivel_dificultad,
ADD COLUMN objetivos TEXT NULL AFTER requisitos,
ADD COLUMN slug VARCHAR(255) UNIQUE NULL AFTER objetivos;

-- 3. Alterar tabla clases para MVP
ALTER TABLE clases
ADD COLUMN descripcion TEXT NULL AFTER titulo,
ADD COLUMN archivos_adjuntos JSON NULL AFTER descripcion,
ADD COLUMN tipo ENUM('video', 'documento', 'quiz', 'tarea', 'live_session') DEFAULT 'video' AFTER archivos_adjuntos,
ADD COLUMN activo BOOLEAN DEFAULT TRUE AFTER tipo,
ADD COLUMN duracion_estimada INT NULL AFTER activo, -- en minutos
ADD COLUMN recursos_adicionales JSON NULL AFTER duracion_estimada,
ADD COLUMN fecha_publicacion TIMESTAMP NULL AFTER recursos_adicionales;

-- 4. Alterar tabla inscripciones para MVP
ALTER TABLE inscripciones
ADD COLUMN estado ENUM('activa', 'completada', 'cancelada', 'expirada') DEFAULT 'activa' AFTER progreso,
ADD COLUMN fecha_expiracion DATE NULL AFTER estado,
ADD COLUMN ultimo_acceso TIMESTAMP NULL AFTER fecha_expiracion,
ADD COLUMN certificado_emitido BOOLEAN DEFAULT FALSE AFTER ultimo_acceso;

-- =============================================================================
-- NUEVAS TABLAS PARA MVP COMPLETO
-- =============================================================================

-- 5. Proveedores OAuth (Google, Facebook, etc.)
CREATE TABLE oauth_providers (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    provider VARCHAR(50) NOT NULL, -- 'google', 'facebook', etc.
    provider_id VARCHAR(255) NOT NULL,
    provider_email VARCHAR(255) NULL,
    access_token TEXT NULL,
    refresh_token TEXT NULL,
    token_expires_at TIMESTAMP NULL,
    profile_data JSON NULL,
    fecha_conexion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY unique_provider_user (usuario_id, provider),
    UNIQUE KEY unique_provider_id (provider, provider_id),
    KEY usuario_id (usuario_id),
    CONSTRAINT oauth_providers_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 6. Sesiones de usuario
CREATE TABLE user_sessions (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    session_token VARCHAR(255) NOT NULL UNIQUE,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    expires_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY usuario_id (usuario_id),
    KEY session_token (session_token),
    KEY expires_at (expires_at),
    CONSTRAINT user_sessions_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 7. Categorías de cursos
CREATE TABLE categorias_cursos (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NULL,
    icono VARCHAR(50) NULL,
    color VARCHAR(7) NULL, -- hex color
    orden INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 8. Tags de cursos
CREATE TABLE tags_cursos (
    id INT NOT NULL AUTO_INCREMENT,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255) NULL,
    color VARCHAR(7) NULL,
    uso_count INT DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY nombre (nombre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 9. Relación curso-tags
CREATE TABLE curso_tags (
    id INT NOT NULL AUTO_INCREMENT,
    curso_id INT NOT NULL,
    tag_id INT NOT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY unique_curso_tag (curso_id, tag_id),
    KEY curso_id (curso_id),
    KEY tag_id (tag_id),
    CONSTRAINT curso_tags_ibfk_1 FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE CASCADE,
    CONSTRAINT curso_tags_ibfk_2 FOREIGN KEY (tag_id) REFERENCES tags_cursos (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 10. Módulos de cursos (agrupar clases)
CREATE TABLE modulos_curso (
    id INT NOT NULL AUTO_INCREMENT,
    curso_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NULL,
    orden INT NOT NULL DEFAULT 1,
    activo BOOLEAN DEFAULT TRUE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY curso_id (curso_id),
    CONSTRAINT modulos_curso_ibfk_1 FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 11. Actualizar tabla clases para incluir modulo_id
ALTER TABLE clases
ADD COLUMN modulo_id INT NULL AFTER curso_id,
ADD KEY modulo_id (modulo_id),
ADD CONSTRAINT clases_ibfk_modulo FOREIGN KEY (modulo_id) REFERENCES modulos_curso (id) ON DELETE SET NULL;

-- 12. Progreso detallado de clases
CREATE TABLE progreso_clases (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    clase_id INT NOT NULL,
    completado BOOLEAN DEFAULT FALSE,
    tiempo_visto DECIMAL(5,2) DEFAULT 0.00, -- en minutos
    porcentaje_completado DECIMAL(5,2) DEFAULT 0.00,
    ultima_visualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    fecha_completado TIMESTAMP NULL,
    notas_personales TEXT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY unique_progreso (usuario_id, clase_id),
    KEY usuario_id (usuario_id),
    KEY clase_id (clase_id),
    CONSTRAINT progreso_clases_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    CONSTRAINT progreso_clases_ibfk_2 FOREIGN KEY (clase_id) REFERENCES clases (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 13. Calificaciones y reseñas de cursos
CREATE TABLE calificaciones_cursos (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    curso_id INT NOT NULL,
    calificacion INT NOT NULL CHECK (calificacion >= 1 AND calificacion <= 5),
    comentario TEXT NULL,
    aspectos_positivos TEXT NULL,
    aspectos_mejorar TEXT NULL,
    recomendado BOOLEAN NULL,
    fecha_calificacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    moderado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id),
    UNIQUE KEY unique_calificacion (usuario_id, curso_id),
    KEY usuario_id (usuario_id),
    KEY curso_id (curso_id),
    CONSTRAINT calificaciones_cursos_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    CONSTRAINT calificaciones_cursos_ibfk_2 FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 14. Sistema de pagos completo
CREATE TABLE pagos (
    id INT NOT NULL AUTO_INCREMENT,
    inscripcion_id INT NOT NULL,
    usuario_id INT NOT NULL,
    monto DECIMAL(10,2) NOT NULL,
    moneda VARCHAR(3) DEFAULT 'USD',
    metodo_pago VARCHAR(50) NOT NULL, -- 'stripe', 'paypal', 'transferencia', etc.
    estado ENUM('pendiente', 'procesando', 'completado', 'fallido', 'reembolsado', 'cancelado') DEFAULT 'pendiente',
    referencia_pago VARCHAR(100) NULL,
    id_transaccion_externa VARCHAR(255) NULL,
    datos_pago JSON NULL, -- información adicional del pago
    fecha_pago TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    notas TEXT NULL,
    procesado_por VARCHAR(100) NULL, -- sistema o usuario que procesó
    PRIMARY KEY (id),
    KEY inscripcion_id (inscripcion_id),
    KEY usuario_id (usuario_id),
    KEY estado (estado),
    KEY fecha_pago (fecha_pago),
    CONSTRAINT pagos_ibfk_1 FOREIGN KEY (inscripcion_id) REFERENCES inscripciones (id) ON DELETE CASCADE,
    CONSTRAINT pagos_ibfk_2 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 15. Cupones de descuento
CREATE TABLE cupones_descuento (
    id INT NOT NULL AUTO_INCREMENT,
    codigo VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR(255) NULL,
    tipo_descuento ENUM('porcentaje', 'monto_fijo') NOT NULL,
    valor_descuento DECIMAL(10,2) NOT NULL,
    limite_uso INT NULL, -- NULL = ilimitado
    usos_actuales INT DEFAULT 0,
    fecha_expiracion DATE NULL,
    activo BOOLEAN DEFAULT TRUE,
    cursos_aplicables JSON NULL, -- IDs de cursos específicos, NULL = todos
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    creado_por INT NULL,
    PRIMARY KEY (id),
    UNIQUE KEY codigo (codigo),
    KEY activo (activo),
    KEY fecha_expiracion (fecha_expiracion),
    KEY creado_por (creado_por),
    CONSTRAINT cupones_descuento_ibfk_1 FOREIGN KEY (creado_por) REFERENCES usuarios (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 16. Uso de cupones
CREATE TABLE uso_cupones (
    id INT NOT NULL AUTO_INCREMENT,
    cupon_id INT NOT NULL,
    usuario_id INT NOT NULL,
    inscripcion_id INT NOT NULL,
    descuento_aplicado DECIMAL(10,2) NOT NULL,
    fecha_uso TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY cupon_id (cupon_id),
    KEY usuario_id (usuario_id),
    KEY inscripcion_id (inscripcion_id),
    CONSTRAINT uso_cupones_ibfk_1 FOREIGN KEY (cupon_id) REFERENCES cupones_descuento (id) ON DELETE CASCADE,
    CONSTRAINT uso_cupones_ibfk_2 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    CONSTRAINT uso_cupones_ibfk_3 FOREIGN KEY (inscripcion_id) REFERENCES inscripciones (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 17. Certificados
CREATE TABLE certificados (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    curso_id INT NOT NULL,
    codigo_certificado VARCHAR(50) NOT NULL UNIQUE,
    nombre_estudiante VARCHAR(255) NOT NULL,
    nombre_curso VARCHAR(255) NOT NULL,
    nombre_profesor VARCHAR(255) NOT NULL,
    fecha_emision TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_completacion TIMESTAMP NULL,
    url_certificado VARCHAR(255) NULL,
    url_verificacion VARCHAR(255) NULL,
    calificacion_final DECIMAL(5,2) NULL,
    horas_completadas DECIMAL(5,2) NULL,
    activo BOOLEAN DEFAULT TRUE,
    PRIMARY KEY (id),
    UNIQUE KEY codigo_certificado (codigo_certificado),
    KEY usuario_id (usuario_id),
    KEY curso_id (curso_id),
    CONSTRAINT certificados_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    CONSTRAINT certificados_ibfk_2 FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 18. Sistema de notificaciones completo
CREATE TABLE notificaciones (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    tipo VARCHAR(50) NOT NULL, -- 'curso_completado', 'nuevo_curso', 'recordatorio', etc.
    titulo VARCHAR(255) NOT NULL,
    mensaje TEXT NOT NULL,
    datos_adicionales JSON NULL,
    leida BOOLEAN DEFAULT FALSE,
    fecha_lectura TIMESTAMP NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_envio TIMESTAMP NULL,
    canal_envio ENUM('email', 'push', 'sms', 'in_app') DEFAULT 'in_app',
    enviado BOOLEAN DEFAULT FALSE,
    PRIMARY KEY (id),
    KEY usuario_id (usuario_id),
    KEY tipo (tipo),
    KEY leida (leida),
    KEY enviado (enviado),
    CONSTRAINT notificaciones_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 19. Lista de deseos
CREATE TABLE lista_deseos (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    curso_id INT NOT NULL,
    fecha_agregado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY unique_wishlist (usuario_id, curso_id),
    KEY usuario_id (usuario_id),
    KEY curso_id (curso_id),
    CONSTRAINT lista_deseos_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    CONSTRAINT lista_deseos_ibfk_2 FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 20. Historial de navegación/cursos vistos recientemente
CREATE TABLE historial_navegacion (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    curso_id INT NOT NULL,
    tipo_actividad ENUM('visualizacion', 'inscripcion', 'finalizacion', 'calificacion') NOT NULL,
    fecha_actividad TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    tiempo_dedicado INT NULL, -- en segundos
    metadata JSON NULL,
    PRIMARY KEY (id),
    KEY usuario_id (usuario_id),
    KEY curso_id (curso_id),
    KEY tipo_actividad (tipo_actividad),
    KEY fecha_actividad (fecha_actividad),
    CONSTRAINT historial_navegacion_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    CONSTRAINT historial_navegacion_ibfk_2 FOREIGN KEY (curso_id) REFERENCES cursos (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 21. Sistema de soporte/chat
CREATE TABLE tickets_soporte (
    id INT NOT NULL AUTO_INCREMENT,
    usuario_id INT NOT NULL,
    titulo VARCHAR(255) NOT NULL,
    descripcion TEXT NOT NULL,
    categoria VARCHAR(50) NULL,
    prioridad ENUM('baja', 'media', 'alta', 'urgente') DEFAULT 'media',
    estado ENUM('abierto', 'en_progreso', 'resuelto', 'cerrado') DEFAULT 'abierto',
    asignado_a INT NULL,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    fecha_cierre TIMESTAMP NULL,
    PRIMARY KEY (id),
    KEY usuario_id (usuario_id),
    KEY asignado_a (asignado_a),
    KEY estado (estado),
    KEY prioridad (prioridad),
    CONSTRAINT tickets_soporte_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE,
    CONSTRAINT tickets_soporte_ibfk_2 FOREIGN KEY (asignado_a) REFERENCES usuarios (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 22. Mensajes de tickets
CREATE TABLE mensajes_ticket (
    id INT NOT NULL AUTO_INCREMENT,
    ticket_id INT NOT NULL,
    usuario_id INT NOT NULL,
    mensaje TEXT NOT NULL,
    es_staff BOOLEAN DEFAULT FALSE,
    archivos_adjuntos JSON NULL,
    fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY ticket_id (ticket_id),
    KEY usuario_id (usuario_id),
    CONSTRAINT mensajes_ticket_ibfk_1 FOREIGN KEY (ticket_id) REFERENCES tickets_soporte (id) ON DELETE CASCADE,
    CONSTRAINT mensajes_ticket_ibfk_2 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 23. Configuraciones del sistema
CREATE TABLE system_settings (
    id INT NOT NULL AUTO_INCREMENT,
    setting_key VARCHAR(100) NOT NULL UNIQUE,
    setting_value TEXT NULL,
    setting_type ENUM('string', 'number', 'boolean', 'json') DEFAULT 'string',
    description VARCHAR(255) NULL,
    category VARCHAR(50) DEFAULT 'general',
    editable BOOLEAN DEFAULT TRUE,
    fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    UNIQUE KEY setting_key (setting_key)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- 24. Logs del sistema
CREATE TABLE system_logs (
    id INT NOT NULL AUTO_INCREMENT,
    nivel ENUM('debug', 'info', 'warning', 'error', 'critical') DEFAULT 'info',
    categoria VARCHAR(50) NULL,
    mensaje TEXT NOT NULL,
    datos_adicionales JSON NULL,
    usuario_id INT NULL,
    ip_address VARCHAR(45) NULL,
    user_agent TEXT NULL,
    fecha_log TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (id),
    KEY nivel (nivel),
    KEY categoria (categoria),
    KEY usuario_id (usuario_id),
    KEY fecha_log (fecha_log),
    CONSTRAINT system_logs_ibfk_1 FOREIGN KEY (usuario_id) REFERENCES usuarios (id) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- =============================================================================
-- DATOS INICIALES PARA MVP
-- =============================================================================

-- Insertar categorías de cursos
INSERT INTO categorias_cursos (nombre, descripcion, icono, color, orden) VALUES
('Medicina y Salud', 'Cursos relacionados con medicina, enfermería y ciencias de la salud', 'fas fa-heartbeat', '#FF6B6B', 1),
('Ingeniería', 'Cursos de ingeniería civil, eléctrica, mecánica y otras especialidades', 'fas fa-cogs', '#4ECDC4', 2),
('Ciencias Sociales', 'Derecho, economía, sociología y ciencias políticas', 'fas fa-balance-scale', '#45B7D1', 3),
('Artes y Humanidades', 'Artes plásticas, música, literatura y filosofía', 'fas fa-palette', '#FFA07A', 4),
('Ciencias Exactas', 'Matemáticas, física, química y ciencias naturales', 'fas fa-atom', '#98D8C8', 5),
('Educación', 'Pedagogía y ciencias de la educación', 'fas fa-graduation-cap', '#F7DC6F', 6),
('Negocios', 'Administración, marketing, finanzas y emprendimiento', 'fas fa-briefcase', '#BB8FCE', 7),
('Tecnología', 'Informática, desarrollo de software y nuevas tecnologías', 'fas fa-code', '#85C1E9', 8);

-- Insertar tags populares
INSERT INTO tags_cursos (nombre, descripcion, color) VALUES
('Programación', 'Desarrollo de software y lenguajes de programación', '#3498db'),
('Bases de Datos', 'SQL, NoSQL y administración de datos', '#e74c3c'),
('Machine Learning', 'Inteligencia artificial y aprendizaje automático', '#9b59b6'),
('Diseño Web', 'HTML, CSS, JavaScript y frameworks frontend', '#1abc9c'),
('Marketing Digital', 'SEO, redes sociales y publicidad online', '#f39c12'),
('Finanzas', 'Contabilidad, inversiones y análisis financiero', '#2ecc71'),
('Idiomas', 'Aprendizaje de idiomas extranjeros', '#e67e22'),
('Salud Mental', 'Psicología y bienestar emocional', '#f1c40f');

-- Configuraciones iniciales del sistema
INSERT INTO system_settings (setting_key, setting_value, setting_type, description, category) VALUES
('site_name', 'SekiWeb - Plataforma Educativa', 'string', 'Nombre del sitio web', 'general'),
('site_description', 'Plataforma educativa para estudiantes ecuatorianos', 'string', 'Descripción del sitio', 'general'),
('contact_email', 'contacto@sekiweb.com', 'string', 'Email de contacto principal', 'general'),
('support_email', 'soporte@sekiweb.com', 'string', 'Email de soporte técnico', 'general'),
('currency', 'USD', 'string', 'Moneda por defecto', 'payments'),
('stripe_public_key', '', 'string', 'Clave pública de Stripe', 'payments'),
('stripe_secret_key', '', 'string', 'Clave secreta de Stripe', 'payments'),
('google_client_id', '', 'string', 'Google OAuth Client ID', 'auth'),
('google_client_secret', '', 'string', 'Google OAuth Client Secret', 'auth'),
('email_verification_required', 'true', 'boolean', 'Requerir verificación de email', 'auth'),
('max_upload_size', '104857600', 'number', 'Tamaño máximo de archivos (bytes)', 'files'), -- 100MB
('allowed_file_types', '["pdf","doc","docx","ppt","pptx","xls","xlsx","txt","jpg","jpeg","png","gif","mp4","avi","mov"]', 'json', 'Tipos de archivo permitidos', 'files'),
('maintenance_mode', 'false', 'boolean', 'Modo mantenimiento activado', 'system'),
('analytics_enabled', 'true', 'boolean', 'Habilitar analytics', 'system'),
('email_notifications_enabled', 'true', 'boolean', 'Habilitar notificaciones por email', 'system');

-- =============================================================================
-- ÍNDICES ADICIONALES PARA RENDIMIENTO
-- =============================================================================

CREATE INDEX idx_cursos_activo ON cursos (activo);
CREATE INDEX idx_cursos_categoria ON cursos (categoria_id);
CREATE INDEX idx_cursos_destacado ON cursos (destacado);
CREATE INDEX idx_cursos_precio ON cursos (precio);
CREATE INDEX idx_clases_curso_orden ON clases (curso_id, orden);
CREATE INDEX idx_inscripciones_usuario ON inscripciones (usuario_id);
CREATE INDEX idx_inscripciones_curso ON inscripciones (curso_id);
CREATE INDEX idx_inscripciones_estado ON inscripciones (estado);
CREATE INDEX idx_progreso_usuario ON progreso_clases (usuario_id);
CREATE INDEX idx_calificaciones_curso ON calificaciones_cursos (curso_id);
CREATE INDEX idx_pagos_estado ON pagos (estado);
CREATE INDEX idx_pagos_fecha ON pagos (fecha_pago);
CREATE INDEX idx_notificaciones_usuario_leida ON notificaciones (usuario_id, leida);
CREATE INDEX idx_certificados_usuario ON certificados (usuario_id);
CREATE INDEX idx_historial_usuario_fecha ON historial_navegacion (usuario_id, fecha_actividad);
CREATE INDEX idx_tickets_estado ON tickets_soporte (estado);
CREATE INDEX idx_logs_fecha ON system_logs (fecha_log);
CREATE INDEX idx_logs_nivel ON system_logs (nivel);

-- =============================================================================
-- CONSTRAINTS Y TRIGGERS ADICIONALES
-- =============================================================================

-- Trigger para actualizar calificación promedio de cursos
DELIMITER ;;
CREATE TRIGGER update_course_rating AFTER INSERT ON calificaciones_cursos
FOR EACH ROW
BEGIN
    UPDATE cursos
    SET calificacion_promedio = (
        SELECT AVG(calificacion)
        FROM calificaciones_cursos
        WHERE curso_id = NEW.curso_id
    ),
    numero_calificaciones = (
        SELECT COUNT(*)
        FROM calificaciones_cursos
        WHERE curso_id = NEW.curso_id
    )
    WHERE id = NEW.curso_id;
END;;
DELIMITER ;

-- Trigger para actualizar contador de estudiantes en cursos
DELIMITER ;;
CREATE TRIGGER update_student_count AFTER INSERT ON inscripciones
FOR EACH ROW
BEGIN
    UPDATE cursos
    SET numero_estudiantes = numero_estudiantes + 1
    WHERE id = NEW.curso_id;
END;;
DELIMITER ;

-- Trigger para logs de auditoría en pagos
DELIMITER ;;
CREATE TRIGGER audit_payment_changes AFTER UPDATE ON pagos
FOR EACH ROW
BEGIN
    IF OLD.estado != NEW.estado THEN
        INSERT INTO system_logs (nivel, categoria, mensaje, datos_adicionales, usuario_id)
        VALUES ('info', 'payments', CONCAT('Estado de pago cambiado: ', OLD.estado, ' -> ', NEW.estado),
                JSON_OBJECT('pago_id', NEW.id, 'monto', NEW.monto, 'estado_anterior', OLD.estado, 'estado_nuevo', NEW.estado),
                NEW.usuario_id);
    END IF;
END;;
DELIMITER ;

-- =============================================================================
-- VISTAS ÚTILES PARA EL MVP
-- =============================================================================

-- Vista de cursos con información completa
CREATE VIEW vista_cursos_completa AS
SELECT
    c.*,
    cat.nombre as categoria_nombre,
    u.nombre as profesor_nombre,
    u.apellido as profesor_apellido,
    ROUND(c.calificacion_promedio, 1) as rating_promedio,
    c.numero_estudiantes,
    c.numero_calificaciones
FROM cursos c
LEFT JOIN categorias_cursos cat ON c.categoria_id = cat.id
LEFT JOIN usuarios u ON c.profesor_id = u.id
WHERE c.activo = TRUE;

-- Vista de estudiantes con progreso
CREATE VIEW vista_estudiantes_progreso AS
SELECT
    u.id,
    u.nombre,
    u.apellido,
    u.email,
    i.curso_id,
    c.titulo as curso_titulo,
    i.progreso,
    i.fecha_inscripcion,
    i.estado,
    COUNT(pc.clase_id) as clases_completadas,
    COUNT(cl.id) as total_clases,
    ROUND((COUNT(pc.clase_id) / COUNT(cl.id)) * 100, 2) as porcentaje_completado
FROM usuarios u
JOIN inscripciones i ON u.id = i.usuario_id
JOIN cursos c ON i.curso_id = c.id
LEFT JOIN clases cl ON c.id = cl.curso_id AND cl.activo = TRUE
LEFT JOIN progreso_clases pc ON u.id = pc.usuario_id AND cl.id = pc.clase_id AND pc.completado = TRUE
WHERE u.activo = TRUE
GROUP BY u.id, u.nombre, u.apellido, u.email, i.curso_id, c.titulo, i.progreso, i.fecha_inscripcion, i.estado;

-- Vista de ingresos por curso
CREATE VIEW vista_ingresos_cursos AS
SELECT
    c.id,
    c.titulo,
    c.precio,
    COUNT(i.id) as total_inscripciones,
    SUM(p.monto) as ingresos_totales,
    AVG(c.calificacion_promedio) as rating_promedio,
    c.numero_estudiantes
FROM cursos c
LEFT JOIN inscripciones i ON c.id = i.curso_id AND i.estado IN ('activa', 'completada')
LEFT JOIN pagos p ON i.id = p.inscripcion_id AND p.estado = 'completado'
GROUP BY c.id, c.titulo, c.precio;

-- =============================================================================
-- PROCEDIMIENTOS ALMACENADOS ÚTILES
-- =============================================================================

-- Procedimiento para crear usuario con OAuth
DELIMITER ;;
CREATE PROCEDURE crear_usuario_oauth(
    IN p_email VARCHAR(150),
    IN p_nombre VARCHAR(100),
    IN p_apellido VARCHAR(100),
    IN p_provider VARCHAR(50),
    IN p_provider_id VARCHAR(255),
    IN p_provider_email VARCHAR(255),
    IN p_profile_data JSON
)
BEGIN
    DECLARE user_id INT;

    -- Insertar usuario si no existe
    INSERT IGNORE INTO usuarios (email, nombre, apellido, rol_id, email_verificado, fecha_creacion)
    VALUES (p_email, p_nombre, p_apellido, 2, TRUE, NOW());

    -- Obtener ID del usuario
    SELECT id INTO user_id FROM usuarios WHERE email = p_email LIMIT 1;

    -- Insertar proveedor OAuth
    INSERT INTO oauth_providers (usuario_id, provider, provider_id, provider_email, profile_data, fecha_conexion)
    VALUES (user_id, p_provider, p_provider_id, p_provider_email, p_profile_data, NOW())
    ON DUPLICATE KEY UPDATE
        profile_data = p_profile_data,
        ultima_actualizacion = NOW();

    -- Log de creación
    INSERT INTO system_logs (nivel, categoria, mensaje, usuario_id)
    VALUES ('info', 'auth', CONCAT('Usuario creado/actualizado via ', p_provider), user_id);

    SELECT user_id as usuario_id;
END;;
DELIMITER ;

-- Procedimiento para procesar pago
DELIMITER ;;
CREATE PROCEDURE procesar_pago(
    IN p_inscripcion_id INT,
    IN p_usuario_id INT,
    IN p_monto DECIMAL(10,2),
    IN p_metodo_pago VARCHAR(50),
    IN p_referencia VARCHAR(100),
    IN p_datos_pago JSON
)
BEGIN
    DECLARE pago_id INT;

    -- Insertar pago
    INSERT INTO pagos (inscripcion_id, usuario_id, monto, metodo_pago, estado, referencia_pago, datos_pago, fecha_pago)
    VALUES (p_inscripcion_id, p_usuario_id, p_monto, p_metodo_pago, 'completado', p_referencia, p_datos_pago, NOW());

    SET pago_id = LAST_INSERT_ID();

    -- Actualizar estado de inscripción
    UPDATE inscripciones SET estado = 'activa' WHERE id = p_inscripcion_id;

    -- Log del pago
    INSERT INTO system_logs (nivel, categoria, mensaje, datos_adicionales, usuario_id)
    VALUES ('info', 'payments', CONCAT('Pago procesado: $', p_monto),
            JSON_OBJECT('pago_id', pago_id, 'inscripcion_id', p_inscripcion_id, 'metodo', p_metodo_pago),
            p_usuario_id);

    SELECT pago_id as pago_id;
END;;
DELIMITER ;

-- Procedimiento para emitir certificado
DELIMITER ;;
CREATE PROCEDURE emitir_certificado(
    IN p_usuario_id INT,
    IN p_curso_id INT
)
BEGIN
    DECLARE cert_code VARCHAR(50);
    DECLARE student_name VARCHAR(255);
    DECLARE course_name VARCHAR(255);
    DECLARE teacher_name VARCHAR(255);
    DECLARE completion_date TIMESTAMP;
    DECLARE final_rating DECIMAL(5,2);

    -- Generar código único
    SET cert_code = CONCAT('CERT-', UPPER(SUBSTRING(MD5(RAND()), 1, 8)), '-', p_usuario_id);

    -- Obtener datos
    SELECT CONCAT(u.nombre, ' ', u.apellido) INTO student_name
    FROM usuarios u WHERE u.id = p_usuario_id;

    SELECT c.titulo INTO course_name
    FROM cursos c WHERE c.id = p_curso_id;

    SELECT CONCAT(u.nombre, ' ', u.apellido) INTO teacher_name
    FROM cursos c JOIN usuarios u ON c.profesor_id = u.id WHERE c.id = p_curso_id;

    SET completion_date = NOW();

    -- Calificación promedio del estudiante en el curso
    SELECT AVG(pc.porcentaje_completado) INTO final_rating
    FROM progreso_clases pc
    JOIN clases cl ON pc.clase_id = cl.id
    WHERE pc.usuario_id = p_usuario_id AND cl.curso_id = p_curso_id;

    -- Insertar certificado
    INSERT INTO certificados (
        usuario_id, curso_id, codigo_certificado, nombre_estudiante,
        nombre_curso, nombre_profesor, fecha_emision, fecha_completacion,
        calificacion_final, activo
    ) VALUES (
        p_usuario_id, p_curso_id, cert_code, student_name,
        course_name, teacher_name, completion_date, completion_date,
        final_rating, TRUE
    );

    -- Actualizar inscripción
    UPDATE inscripciones SET certificado_emitido = TRUE WHERE usuario_id = p_usuario_id AND curso_id = p_curso_id;

    -- Notificación
    INSERT INTO notificaciones (usuario_id, tipo, titulo, mensaje)
    VALUES (p_usuario_id, 'certificado', '¡Certificado emitido!',
            CONCAT('Felicitaciones! Has completado el curso "', course_name, '" y tu certificado está listo.'));

    SELECT cert_code as codigo_certificado;
END;;
DELIMITER ;</content>
<parameter name="filePath">e:/DOCUMENTOS/U/3semestre/base_de_datos/PROYECTO1/SekiWeb/expand_database.sql