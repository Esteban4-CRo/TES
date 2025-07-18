PGDMP  7                    }            emotionalai    17.4    17.4 $               0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                           false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                           false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                           false                       1262    16388    emotionalai    DATABASE     q   CREATE DATABASE emotionalai WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en-US';
    DROP DATABASE emotionalai;
                     postgres    false            �            1259    16414    comentarios    TABLE     �   CREATE TABLE public.comentarios (
    id_comentario integer NOT NULL,
    contenido character varying,
    id_usuario integer,
    id_profesional integer,
    archivo bytea,
    fecha date DEFAULT CURRENT_DATE
);
    DROP TABLE public.comentarios;
       public         heap r       postgres    false            �            1259    16413    comentarios_id_comentario_seq    SEQUENCE     �   CREATE SEQUENCE public.comentarios_id_comentario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 4   DROP SEQUENCE public.comentarios_id_comentario_seq;
       public               postgres    false    222                       0    0    comentarios_id_comentario_seq    SEQUENCE OWNED BY     _   ALTER SEQUENCE public.comentarios_id_comentario_seq OWNED BY public.comentarios.id_comentario;
          public               postgres    false    221            �            1259    16436    personas    TABLE     H   CREATE TABLE public.personas (
    documento_identidad text NOT NULL
);
    DROP TABLE public.personas;
       public         heap r       postgres    false            �            1259    16401    profesionales    TABLE     T  CREATE TABLE public.profesionales (
    id_profesional integer NOT NULL,
    nombre character varying(200),
    documento_identidad text,
    contrasena character varying NOT NULL,
    certificado bytea NOT NULL,
    perfil bytea NOT NULL,
    correo character varying(200),
    descripcion character varying(600),
    especialidad text
);
 !   DROP TABLE public.profesionales;
       public         heap r       postgres    false            �            1259    16400     profesionales_id_profesional_seq    SEQUENCE     �   CREATE SEQUENCE public.profesionales_id_profesional_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 7   DROP SEQUENCE public.profesionales_id_profesional_seq;
       public               postgres    false    220                       0    0     profesionales_id_profesional_seq    SEQUENCE OWNED BY     e   ALTER SEQUENCE public.profesionales_id_profesional_seq OWNED BY public.profesionales.id_profesional;
          public               postgres    false    219            �            1259    16390    usuarios    TABLE     �   CREATE TABLE public.usuarios (
    id_usuario integer NOT NULL,
    nombre character varying(200),
    documento_identidad text,
    correo character varying(200),
    contrasena character varying NOT NULL
);
    DROP TABLE public.usuarios;
       public         heap r       postgres    false            �            1259    16389    usuarios_id_usuario_seq    SEQUENCE     �   CREATE SEQUENCE public.usuarios_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 .   DROP SEQUENCE public.usuarios_id_usuario_seq;
       public               postgres    false    218                       0    0    usuarios_id_usuario_seq    SEQUENCE OWNED BY     S   ALTER SEQUENCE public.usuarios_id_usuario_seq OWNED BY public.usuarios.id_usuario;
          public               postgres    false    217            g           2604    16417    comentarios id_comentario    DEFAULT     �   ALTER TABLE ONLY public.comentarios ALTER COLUMN id_comentario SET DEFAULT nextval('public.comentarios_id_comentario_seq'::regclass);
 H   ALTER TABLE public.comentarios ALTER COLUMN id_comentario DROP DEFAULT;
       public               postgres    false    221    222    222            f           2604    16404    profesionales id_profesional    DEFAULT     �   ALTER TABLE ONLY public.profesionales ALTER COLUMN id_profesional SET DEFAULT nextval('public.profesionales_id_profesional_seq'::regclass);
 K   ALTER TABLE public.profesionales ALTER COLUMN id_profesional DROP DEFAULT;
       public               postgres    false    220    219    220            e           2604    16393    usuarios id_usuario    DEFAULT     z   ALTER TABLE ONLY public.usuarios ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuarios_id_usuario_seq'::regclass);
 B   ALTER TABLE public.usuarios ALTER COLUMN id_usuario DROP DEFAULT;
       public               postgres    false    218    217    218                      0    16414    comentarios 
   TABLE DATA           k   COPY public.comentarios (id_comentario, contenido, id_usuario, id_profesional, archivo, fecha) FROM stdin;
    public               postgres    false    222   �-                 0    16436    personas 
   TABLE DATA           7   COPY public.personas (documento_identidad) FROM stdin;
    public               postgres    false    223   �-                 0    16401    profesionales 
   TABLE DATA           �   COPY public.profesionales (id_profesional, nombre, documento_identidad, contrasena, certificado, perfil, correo, descripcion, especialidad) FROM stdin;
    public               postgres    false    220   �-                 0    16390    usuarios 
   TABLE DATA           _   COPY public.usuarios (id_usuario, nombre, documento_identidad, correo, contrasena) FROM stdin;
    public               postgres    false    218   �Q                  0    0    comentarios_id_comentario_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.comentarios_id_comentario_seq', 1, true);
          public               postgres    false    221                       0    0     profesionales_id_profesional_seq    SEQUENCE SET     N   SELECT pg_catalog.setval('public.profesionales_id_profesional_seq', 3, true);
          public               postgres    false    219                        0    0    usuarios_id_usuario_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.usuarios_id_usuario_seq', 4, true);
          public               postgres    false    217            v           2606    16422    comentarios comentarios_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.comentarios
    ADD CONSTRAINT comentarios_pkey PRIMARY KEY (id_comentario);
 F   ALTER TABLE ONLY public.comentarios DROP CONSTRAINT comentarios_pkey;
       public                 postgres    false    222            x           2606    16442    personas personas_pkey 
   CONSTRAINT     e   ALTER TABLE ONLY public.personas
    ADD CONSTRAINT personas_pkey PRIMARY KEY (documento_identidad);
 @   ALTER TABLE ONLY public.personas DROP CONSTRAINT personas_pkey;
       public                 postgres    false    223            p           2606    16468 3   profesionales profesionales_documento_identidad_key 
   CONSTRAINT     }   ALTER TABLE ONLY public.profesionales
    ADD CONSTRAINT profesionales_documento_identidad_key UNIQUE (documento_identidad);
 ]   ALTER TABLE ONLY public.profesionales DROP CONSTRAINT profesionales_documento_identidad_key;
       public                 postgres    false    220            r           2606    16408     profesionales profesionales_pkey 
   CONSTRAINT     j   ALTER TABLE ONLY public.profesionales
    ADD CONSTRAINT profesionales_pkey PRIMARY KEY (id_profesional);
 J   ALTER TABLE ONLY public.profesionales DROP CONSTRAINT profesionales_pkey;
       public                 postgres    false    220            t           2606    16482 "   profesionales unique_documento_pro 
   CONSTRAINT     l   ALTER TABLE ONLY public.profesionales
    ADD CONSTRAINT unique_documento_pro UNIQUE (documento_identidad);
 L   ALTER TABLE ONLY public.profesionales DROP CONSTRAINT unique_documento_pro;
       public                 postgres    false    220            j           2606    16448 !   usuarios unique_documento_usuario 
   CONSTRAINT     k   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT unique_documento_usuario UNIQUE (documento_identidad);
 K   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT unique_documento_usuario;
       public                 postgres    false    218            l           2606    16446 )   usuarios usuarios_documento_identidad_key 
   CONSTRAINT     s   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_documento_identidad_key UNIQUE (documento_identidad);
 S   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_documento_identidad_key;
       public                 postgres    false    218            n           2606    16397    usuarios usuarios_pkey 
   CONSTRAINT     \   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT usuarios_pkey PRIMARY KEY (id_usuario);
 @   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT usuarios_pkey;
       public                 postgres    false    218            {           2606    16428 +   comentarios comentarios_id_profesional_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.comentarios
    ADD CONSTRAINT comentarios_id_profesional_fkey FOREIGN KEY (id_profesional) REFERENCES public.profesionales(id_profesional);
 U   ALTER TABLE ONLY public.comentarios DROP CONSTRAINT comentarios_id_profesional_fkey;
       public               postgres    false    222    220    4722            |           2606    16423 '   comentarios comentarios_id_usuario_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.comentarios
    ADD CONSTRAINT comentarios_id_usuario_fkey FOREIGN KEY (id_usuario) REFERENCES public.usuarios(id_usuario);
 Q   ALTER TABLE ONLY public.comentarios DROP CONSTRAINT comentarios_id_usuario_fkey;
       public               postgres    false    218    222    4718            z           2606    16483 $   profesionales fk_profesional_persona    FK CONSTRAINT     �   ALTER TABLE ONLY public.profesionales
    ADD CONSTRAINT fk_profesional_persona FOREIGN KEY (documento_identidad) REFERENCES public.personas(documento_identidad);
 N   ALTER TABLE ONLY public.profesionales DROP CONSTRAINT fk_profesional_persona;
       public               postgres    false    4728    223    220            y           2606    16476    usuarios fk_usuario_persona    FK CONSTRAINT     �   ALTER TABLE ONLY public.usuarios
    ADD CONSTRAINT fk_usuario_persona FOREIGN KEY (documento_identidad) REFERENCES public.personas(documento_identidad);
 E   ALTER TABLE ONLY public.usuarios DROP CONSTRAINT fk_usuario_persona;
       public               postgres    false    4728    223    218                  x������ � �         !   x�342�2440711531�2101������ :3)            x��ɒ,�u���S�k��a'�L�J&R4iō�"ȶ�4��H��z���?"�*�*o�m6�� 2�=|8~��x�������W������>��/�	����Y�g�/��o�����_��_�ſ�����)������ۿ�����������������m�_�����P�������,{/c�5��jHǉ�&��oa8O.�\RM
c�����Q�h�u��u�^���߮+�����ztƺ�.w9���9�|���9�%����l#�t��|%i<��V����6�dl�}���t�n��y;t�7�{�\v�5Wm��Mo�t�mt���5'�H5����J�zW���	���&�T默��k�;�->��*��ֆ?y�����A�|=Y/�z�~ۓ��ǌ#�Z��˴�[���R�t��4c���p[Z��G�F���K�wɦ��D�EG���\�I��(g��RCSԫuq��a����y �z�C�p�2�j���h��]�Mg�gD��	�;J$�c�1��ݖZC�&���#�og�Aj1�+�([<KAnJ<��M����U:onw���c�W��\�����ۖ�����H���q�jI
^U3\T�֧6K/G�.�eƮ�h�g�H�]a�Zƙ&%�"f�#+Ȏ�d�X=��j�۴�J����{�3��Vt[���e7J�I~k7E�&ܜV�GT�d}Yv�n���	�w�hB�kk�쓿�n�D�	mb�/�c1W�ճ�}��g��];�hl�RG̋��RX~���!�XB?W*;W�9n����i��*t�	��@�t(_�.\ڡ#�dd4�t���Ʊ�XY�SDNF�0:��C�ʴk������Kz��Pb�t[W�j�WN���sH���U��� �9~�<�5P�ȯ��5�h��>+�'$4�(m��=����R�#��*k��&�H�a�e/�%X{��@��Y���i?:���iΏ ŕ�q�Yx}�TE��Ҕa�%��X���ܱ���POst}"qr�Ï\����i�2�г� :� ����-ػ-jg����~۩;{������3l6�F����R/æ]ڰ�����
<�vl��\����g��nG�o[ L��aVOHcW��Ѫ�a�mJA����W�_� �s��Iڕ��Ƽ������<23K�yp7����p�P��C75���2���
r��L
b �aR����ݎ��4�h"�󏙥��@��P&dx�7)2şɬ�z��Ɣ���ݨ5!�M���Pam�Q�!O�G�)O�T���J`%�.-Xr�H��������"�tǩ��V�˱s���wdX��qC��M���L�Z�	چ��{aZpO�X���)�U�oͳ̻Mi!H�y-��kB���N���G�	�"��KT!Q�E�6�ʥB�0�[m������!1�n,��z�����ʩ�+$�K���2�o((m��R}� ّ9�,{Dv����$Qd*fOɐ3uZs�!qR��s�k�� �]�6�������X��>�'�/ۑ#���r��nQQ�c�k��l)C�s<��`����A�0�$yt���naӞM�8��3��.��u�WNi჌�r�y��6�jc�C�|ڭ�>뚧|y*d�N̡V��c�ة����*N�ẖ��,K�!S����!�p���[$+~�4�쫑46$�2x&�J��E܋0&w�,�9�P��4'�C�Ä�c �$m?��T/3%i����/I��',�M���.-=&���Bp<�D��Zy�\f�x�!�%5�#��)�!������,&H���_��bK��6�)(W!�˔�ө��C�I��K"kG!��A��!'�r_M:�R��P[�Nh7�"'�� ���@���H�h+.�j����N"D5��8�٢ɝ�y͋?���[
C7\|� L\�B���.�'�u ��@���Os!%U�j���0�3-,[2��l���bW�͡;6uK�Ϧ��MQ��i#��i9P{��@��[8��2~����l���%����{������u}9ٲsZ� 
�e�	���6kK4=��"5v{;�	k;�:Z��ȅ�2l(g��d��l��4��7�z�nH��[��xcđ��
8�����[�`c��((��r7��S�Z�b��g
>��Ja����6>�k�@��ɥZU�R6��q�r����x�8�l 1���?���١
���jXߣ�3��q�����׾<��J�m@Q�xn�;�Q�	[Qd�pڥ���o�2�A�߿޼�=�5����P�my�ܥg��Z���<�Z�������G첂�j�+W\���2v7���ߝ ���̑��u� (`)��%��4�_@{�7_ z l�^�,��p�l�z C�z�ף�  eMjg�r>��d�p���)�S(���u/+sЅ�S��B}��
�����f��J���x���sq"	U	'ⴛP��Քb�|��K�:�A6����.���5��[sL�5��v�h���$�^�>�f�^茹�pB�j�:�N~��P�E�Ր�����a����$���{2 3 2��8a�Xd���@0ފ#�s�3\�އ0��]�˗w2�.���ɰ~V�Qp���.��`-��=#����V�O���{2"�{dۂ��T[f{p�y8�"�8H�YV ��pQ!�^X�B�r�s6>�]&�倥�􏞮R*R9�.�`��pv�ʥ#�N����Kr��Fs�A�?�����MKM&.V���G[q���k>������C��6��"���o9�R��V���Z�D����W[���ѱQJw�t]���z�h�
F�!|�פѼ\;|!%cH��V������ѯ����E�2�{!U��Ā�p;H9��aw��w��k���z�c[���^�o�ȁ���.�T�kl���.!##��Y��(NZ�qQ�d��������&,j�E�M��6|���ˆ�zFۤ�.w�<"���;��xt��M���l�����xـ8�:��A�һp�O'\Ru��*�{���'��4mq{�7������$=T��9�-gbqn����ъ�@��0��a=
����9��z�<���W�1�ׁ�)��$��FK&��V��+�aK�~�%�k�vf�Y~����'ڣ���r�1��$�������fs�%^���[����oJy�Y����F��.NgH�ݡ�	��`o���n���f],��}2�m�@82�X��'^�w1��\�WC	,w}cΖwc��zw�����.�so�X��E��A�ˮ��/;7��͸k���6|J��u�0��T���n՝K�����N=r!���nĉ���;� )1NcOk�J�ִ7�A?������[��z�(�r�ʾG:H1mT��7��V$#p�"��F��L���*�Fi��*�^|�1^ȥ��qV���u�������l�pGO/�9�Uo'�µ�,m�ޓţ���[��F/vpJ��[@ ����A'���q�[����p�j9��:�n;��zc�3�B��64���;齒@����-�It�����/�������/>=\.��V�{�N��E���@�^!R�>qu�;L����L<ch����a_tM�&h���σ1�DX��q&LSDݑ&�A�f_;�=kޮ�eӆ��P����-��X�饑?=��^����jm-�v���d}����/��9oMG3ԃ{jx��\�zh+�7�FtP�ה(�kg���]�}��W��vS�>s1�Q�4C\:D���P�Zt�Ҽn��t��yp"^�db؋�am|��PÞ9[�2��ڊ.�&c��%/������oLȇ�)�P�«[��<4�N������Q�a��'�wۃ�C�͇M�UT����7^���[K���R��P��b@�p�� %�(�ZþPu�ݚz����q28���B�d�ՙӎ#z���)�P����O��?$��:b(K�����k�u��@/��&cM]�G>p��=��TcjW���S|�d;�%;�4�z    ub���&a.�<��L~Oн|i0�L�&XF@�����z_sT�D����Hvǝ��c�cU׌�Rd(�E[�Pqs������;��Ĥ�Vg�r��o�'enl
θ*��wӗ���Rs��(b�
~�0F���D8��˓7`�.%7�Z{@�Q0%��@gh{��6�V�z����O���ݙ�Gf�w��?$&b6a�7��Aw�'8a��{����վ��sDY@������_���er��զ4ߟ��)��^ �'�~{��u��;�Wy�sY�Iɸ����E|8���Zi�+�+nڟ�%T�z�����_�)�}�O�ۍfQ:�{�0cv`{(�3/��r��.��QJ�8�s4�# h=��*�i�F��y���/b1�r3O�:L�w����I,<3DP�zP͑k�:k�tv
��g��.�$�^�Q��C���!����g�3��`�m"�ղl���zMdׇ7�X\ۛ/�A�E?�����mF�*���������Hy���#��έ�֏�JAh�ƕ,�����>�S}Ma����E�1�z���~�3�z��"�Yy�>�C�X����M�kv;ː�:jᙩ)��<͏���̶	i���zU�h���"0dJ���RC}o>� ��:�GR ����	A[~�uenB���K�R��īL8��e�ORPN��8��u{D�Sw���X�f&y~%���2�{��mِ�r��� R�U���礼�j��` ����^t|��U��i`����W��[�e޲�a`Ts��'�H�+\`��n4I/��|tɣ%4�1Kˏ��z�+�w֥^WG\�9����B�/�ܞ�v�� |���ײDz�\�EB�BH���}-br�[�&̻���-C}�
��WY�g��)��<EkUv�!���*�S�"�/�P�$y���i���I�=�~�P�a��h�}�9`�> ����'�T��?�C3�8����%����{p[���N��ї,�.�aP����z�@�͡�`+u�GCݝ����H��x[�Ʒ�����X�����	r�p�-(I*ݩ禚y�A1۩+4�N����#rQ]V2 �0y.f�M��L��#kMZ����ؗ�a��֍���<�0h���t��+"ei���ߝ�|f���{��c@���t�gU�
�1o�Cx|lO�����Gp|*j����%���Ӯe��r��㨳-�Ƥ�CvVr��N�RmԀ�̓SK�,�gzi�S*���i%���'@�
 ���ƭ�I:%`�dA%E�x��ą�&�l�T�1��w��w����f�j5V�F�����_�w�}��.5u��~���Wٶ���+A�_W5�n�ܭ�P�{n�4�F �(<�C%��J+}��%��Fƥ
�O�@)6\���C�B���U������v�Kxwa�=�~h �G�UOu�F�h��~�1����� �T��{�#Ȃ�ͣ�p��d��]}?j��m�k���wu���{��4�ԌWw����K�l,ϻ�_=���{��K9��!DW�}��&U@��X�c��� �3&��>��vc�+�״[�R=�����[�͹�@�_���3}�qw�wW+�QJi,�5���E����f��fw���H��u��<���n�Y�����C8x�<�C8��=�O�f�W{/�帟)�+�]�g4a���{~+�|�+�����~�5��W�D�>?��A��W4�������}�{i|�q��NYw�&/Eao�޼�i;�5������[t��y��fwϟQ�Ũ���<� �ӫ
<�YY�\�x��S���[d�ک"���:~Kcޔ%�z��wr�Y��o���.��/��w�:�~ʇFԠ���HQ$\�$;�I�+�K��K\����!<�U�gF~��,��sǃ9b�	���i�8�Y�m��V��tʔ�1�5y�=X��Sr��\W�������>A������Gӫ7�,n��6=��f��Dޥ�<g.��L	]���r�B[~�5B�G�i�a~s�U��ܾS�jU��a�ǡ)��-L�ͣ��ˉ���|��B)���嵄�`C�7~.[���;��Vξ��>R���5�1�%�8���]�c��r�6�$t�*�����Jʸ��P���éÂi����<���^����}�5:�klߎ�Ţ��5�����n��+�r�A�6���H��m�bG����T85,[���5�MX>�dc}!_�ei@/Қ�Pl�5���V3��{�F3
�$��z{��l�&�j��p�̽����m���������&�fA�Ǜ����Nw[c�j8 u�m�zMO>v �S�74幠����yY)�����j�:JW�ˬWרs�5��*ZO�!��NI�x�����z�6r׵Sܩ�ך�:9���]�|S�V,[W��ͪ7��ÅF_y�͗�`7B���^e�ʿl��;����Y�9������y�,I˙����$�wz�׭���5SlMp�
j5M�ҝ����YB;�[�Q�G^����L1x�	��躖�5 ������2W���F�e���B֬A�b����y�����KT����hjy��/����hhq���5SM�V������;^r>zSi1Xؖ�:�o��xN(�p\�7sf�a뾝s��YcF�;zM��s<g�@���8��	{N��cG��,4���{��5��x��Gn[-3 �w'��q�cT�`�Ѹps��0s9���^ϭЫlM�[�s���_ޝ��2�A�j�Ӫ�ށ�!���U�R^̄������`�|�s�Cy0�)}�]2�b^D���i��[�����4oG�9:�w�؅kiC^��T�s]U54v���0���]?�&�g�"�A�@-u��B�z�F�t���ٵJ������RR���Q&�P�{���Ω����;�<R���s>�GB�oD�9��`��r��%�>V��K^C��dB(.���Cѯaڬ�D������kh�$z��k8WJ{��*��F��FgP갋|��Y5̾)���f!7�Y���po��`���4{qރ�����M+�x[��F�i材�]ꩂ�0��޸��e��@+��k,-�Lt��Q#
O(Zud�iX[�MhU9���Y$�\�*�O8ӧ�at(K�c�����	�<�s��@A��v�c2m߲�<"ՋS�k0��3ژ����l���D1�
���v����y�����~��𢝚��ڣ�DQ�&G�jVT��x�6��?f!�����e@��Ea,/�i�QyxaY=��$ŁZ &D�7��4m�)�����	����]�Q}0�+s�Q3�@��@��.�{�z��W$�󎌢��z����N��	u� �h�v��YN��ꉊ�}��X� �^�%���.hl�=��t���K��j�*���b���-D4��ۦ4���>7�H0��?�1��Ԣ�vh��*�N7�/�W����h�c�;�j�c�i(�Q0��-����IǠ~�6�VoV�Ý�;O�Nݤ���zK��>�rC�>A�=�����	�Ccp��>�g~�w0��_��֚����q0ꤪp5��^5&��Yewt�tyiV�����Gxp�#]�Sd]����[jV8���#�`��w�tr���Ϥ�0��C��/I��X
@��&�Q�{���c$�!�>���T��[�˖�C��c�Kr0��� �#yD���a����s+?7����jTc˕1=�7����������tis��{j�Ո�+A��GV��m>�����J�Ncڜ���v̈́U+�ft��E�[Ɲ�~�uxbV�ٓ���\�`}x��!.u�Ȁ�����a]%���Qd5	�i�J���:����5���ʁ/�܇�&������	�T�X��Qx�3���{w����~���,�}��9��0�s�m�"�R���)��f�A��F�$��D`�f�a��a'��%<0͕������1lc9^��ԣ5�����������a7UC
fmx�@�<4�%������� �  �����W��ύ?����lN�x�kB[�v��J]ӵ/͜�
�U��u���mcW�jRcI��H�Z�?��J�Λw߈l�+�y�<��Zy4As?-�pE�QJ4T�u��S�H�f��3�^�^�C�\�]Ҝ�80x��D�8%������g��V�Y:-��J �&�������Op����'�_�O��6��gQ�u�zR�?�B���[4^��zb�d��!�}9��V
�����~�����Aa��T{�b߾�D����ɂ,9�:���Q���Y�g�fU�����䘒��iJe+����|��l����ӿM��D���$x=�a�|!�2�O6�}ىf��j/���(Y<f ���̀+�4Y��dT��t{��8�����v�iƅ�r�������a��X��4��fg#����q��ШOȫ	nq��C�@n��^�NN��0Q+_���<�_�����R�Q%�q�4i���������N2� ;{��\�蹎�s���\��3~�c�\�蹎���B�u���=�1z�c�\��<�1z�c�\�蹎�s��Z�u����}��=�1z�c�\�蹎�s��:F�u����Q�~�c�\��'�s�?�p�u�~~���=�1z�c�\�蹎�s��:F�u���=�1z�c�\�蹎�s����D�u���=�1z�c�\�蹎�s��:F�u���=�1z�c��_�蹎�s��:F�u���}Q��=�1z�c�\�蹎�s��:F�u���=�1z�c�\�Ș�:F�u����l#~�c�\�蹎�s��:F�u���=�1�����s��:F�u����i�}�c�\�蹎�s��:Fz�������Ƨ��f}��7�������Wk��W��/��ӿ|��o����|��~����W뛯��~=>}�����m_�O�|� ����O�i��Ws}�u�J1���ïg�\���3گ~���_���~��_�lS<o         �   x�e�I�0 �u{ք�Ɲ�C� J�M��-�(���.�(����D�HH�ՉF
���]�j+����"/�<z��kS����t��.{[��W��ܛ$�o��1M��~�W�)�	 Q�Z����HF�����&�Ez��C�<�0��L���n'���d���n:E�>��Z?�     