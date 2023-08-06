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

#ifndef YY_YY_Y_TAB_H_INCLUDED
# define YY_YY_Y_TAB_H_INCLUDED
/* Debug traces.  */
#ifndef YYDEBUG
# define YYDEBUG 0
#endif
#if YYDEBUG
extern int yydebug;
#endif

/* Token type.  */
#ifndef YYTOKENTYPE
# define YYTOKENTYPE
  enum yytokentype
  {
    NUMBER = 258,
    SIDED_DIE = 259,
    FATE_DIE = 260,
    REPEAT = 261,
    SIDED_DIE_ZERO = 262,
    EXPLOSION = 263,
    IMPLOSION = 264,
    PENETRATE = 265,
    ONCE = 266,
    MACRO_ACCESSOR = 267,
    MACRO_STORAGE = 268,
    SYMBOL_SEPERATOR = 269,
    ASSIGNMENT = 270,
    KEEP_LOWEST = 271,
    KEEP_HIGHEST = 272,
    DROP_LOWEST = 273,
    DROP_HIGHEST = 274,
    FILTER = 275,
    LBRACE = 276,
    RBRACE = 277,
    PLUS = 278,
    MINUS = 279,
    MULT = 280,
    MODULO = 281,
    DIVIDE_ROUND_UP = 282,
    DIVIDE_ROUND_DOWN = 283,
    REROLL = 284,
    SYMBOL_LBRACE = 285,
    SYMBOL_RBRACE = 286,
    STATEMENT_SEPERATOR = 287,
    CAPITAL_STRING = 288,
    DO_COUNT = 289,
    MAKE_UNIQUE = 290,
    NE = 291,
    EQ = 292,
    GT = 293,
    LT = 294,
    LE = 295,
    GE = 296,
    RANGE = 297,
    UMINUS = 298
  };
#endif
/* Tokens.  */
#define NUMBER 258
#define SIDED_DIE 259
#define FATE_DIE 260
#define REPEAT 261
#define SIDED_DIE_ZERO 262
#define EXPLOSION 263
#define IMPLOSION 264
#define PENETRATE 265
#define ONCE 266
#define MACRO_ACCESSOR 267
#define MACRO_STORAGE 268
#define SYMBOL_SEPERATOR 269
#define ASSIGNMENT 270
#define KEEP_LOWEST 271
#define KEEP_HIGHEST 272
#define DROP_LOWEST 273
#define DROP_HIGHEST 274
#define FILTER 275
#define LBRACE 276
#define RBRACE 277
#define PLUS 278
#define MINUS 279
#define MULT 280
#define MODULO 281
#define DIVIDE_ROUND_UP 282
#define DIVIDE_ROUND_DOWN 283
#define REROLL 284
#define SYMBOL_LBRACE 285
#define SYMBOL_RBRACE 286
#define STATEMENT_SEPERATOR 287
#define CAPITAL_STRING 288
#define DO_COUNT 289
#define MAKE_UNIQUE 290
#define NE 291
#define EQ 292
#define GT 293
#define LT 294
#define LE 295
#define GE 296
#define RANGE 297
#define UMINUS 298

/* Value type.  */
#if ! defined YYSTYPE && ! defined YYSTYPE_IS_DECLARED
union YYSTYPE
{
#line 96 "src/grammar/dice.yacc"

    vec values;

#line 147 "y.tab.h"

};
typedef union YYSTYPE YYSTYPE;
# define YYSTYPE_IS_TRIVIAL 1
# define YYSTYPE_IS_DECLARED 1
#endif


extern YYSTYPE yylval;

int yyparse (void);

#endif /* !YY_YY_Y_TAB_H_INCLUDED  */
