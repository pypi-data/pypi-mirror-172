/* A Bison parser, made by GNU Bison 3.5.1.  */

/* Bison interface for Yacc-like parsers in C

   Copyright (C) 1984, 1989-1990, 2000-2015, 2018-2020 Free Software Foundation,
   Inc.

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

/* As a special exception, you may create a larger work that contains
   part or all of the Bison parser skeleton and distribute that work
   under terms of your choice, so long as that work isn't itself a
   parser generator using the skeleton or a modified version thereof
   as a parser skeleton.  Alternatively, if you modify or redistribute
   the parser skeleton itself, you may (at your option) remove this
   special exception, which will cause the skeleton and the resulting
   Bison output files to be licensed under the GNU General Public
   License without this special exception.

   This special exception was added by the Free Software Foundation in
   version 2.2 of Bison.  */

/* Undocumented macros, especially those whose name start with YY_,
   are private implementation details.  Do not rely on them.  */

#ifndef YY_IGRAPH_PAJEK_YY_HOME_RUNNER_WORK_PYTHON_IGRAPH_PYTHON_IGRAPH_VENDOR_BUILD_IGRAPH_SRC_IO_PARSERS_PAJEK_PARSER_H_INCLUDED
# define YY_IGRAPH_PAJEK_YY_HOME_RUNNER_WORK_PYTHON_IGRAPH_PYTHON_IGRAPH_VENDOR_BUILD_IGRAPH_SRC_IO_PARSERS_PAJEK_PARSER_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int igraph_pajek_yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    END = 0,
    NEWLINE = 258,
    NUM = 259,
    ALNUM = 260,
    QSTR = 261,
    PSTR = 262,
    NETWORKLINE = 263,
    NET_TITLE = 264,
    VERTICESLINE = 265,
    ARCSLINE = 266,
    EDGESLINE = 267,
    ARCSLISTLINE = 268,
    EDGESLISTLINE = 269,
    MATRIXLINE = 270,
    ERROR = 271,
    VP_X_FACT = 272,
    VP_Y_FACT = 273,
    VP_IC = 274,
    VP_BC = 275,
    VP_LC = 276,
    VP_LR = 277,
    VP_LPHI = 278,
    VP_BW = 279,
    VP_FOS = 280,
    VP_PHI = 281,
    VP_R = 282,
    VP_Q = 283,
    VP_LA = 284,
    VP_FONT = 285,
    VP_URL = 286,
    VP_SIZE = 287,
    EP_C = 288,
    EP_S = 289,
    EP_A = 290,
    EP_W = 291,
    EP_H1 = 292,
    EP_H2 = 293,
    EP_A1 = 294,
    EP_A2 = 295,
    EP_K1 = 296,
    EP_K2 = 297,
    EP_AP = 298,
    EP_P = 299,
    EP_L = 300,
    EP_LP = 301,
    EP_LR = 302,
    EP_LPHI = 303,
    EP_LC = 304,
    EP_LA = 305,
    EP_SIZE = 306,
    EP_FOS = 307
  };
#endif

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{

  igraph_integer_t intnum;
  igraph_real_t    realnum;
  struct {
    char *str;
    size_t len;
  } string;


};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif

/* Location type.  */
#if ! defined YYLTYPE && ! defined YYLTYPE_IS_DECLARED
typedef struct YYLTYPE YYLTYPE;
struct YYLTYPE
{
  int first_line;
  int first_column;
  int last_line;
  int last_column;
};
# define YYLTYPE_IS_DECLARED 1
# define YYLTYPE_IS_TRIVIAL 1
#endif



int igraph_pajek_yyparse (igraph_i_pajek_parsedata_t* context);

#endif /* !YY_IGRAPH_PAJEK_YY_HOME_RUNNER_WORK_PYTHON_IGRAPH_PYTHON_IGRAPH_VENDOR_BUILD_IGRAPH_SRC_IO_PARSERS_PAJEK_PARSER_H_INCLUDED  */
